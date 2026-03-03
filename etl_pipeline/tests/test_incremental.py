import textwrap
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from extract import _filter_since, extract
from load import PIPELINE_NAME, WATERMARK_COLUMN


class TestFilterSince:
    def _df(self, dates):
        return pd.DataFrame({"order_date": dates, "order_id": range(len(dates))})

    def test_filters_rows_before_watermark(self):
        wm = datetime(2024, 1, 20, tzinfo=timezone.utc)
        df = self._df(["2024-01-18", "2024-01-19", "2024-01-20", "2024-01-21"])
        result = _filter_since(df, wm)
        assert len(result) == 1
        assert result.iloc[0]["order_date"] == "2024-01-21"

    def test_watermark_date_excluded(self):
        wm = datetime(2024, 1, 20, tzinfo=timezone.utc)
        assert len(_filter_since(self._df(["2024-01-20"]), wm)) == 0

    def test_all_rows_after_watermark_kept(self):
        wm = datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert (
            len(_filter_since(self._df(["2024-01-10", "2024-01-15", "2024-01-20"]), wm))
            == 3
        )

    def test_all_rows_before_watermark_dropped(self):
        wm = datetime(2024, 12, 31, tzinfo=timezone.utc)
        assert len(_filter_since(self._df(["2024-01-10", "2024-01-15"]), wm)) == 0

    def test_unparseable_dates_dropped(self):
        wm = datetime(2024, 1, 1, tzinfo=timezone.utc)
        result = _filter_since(self._df(["not-a-date", "2024-01-15"]), wm)
        assert len(result) == 1
        assert result.iloc[0]["order_date"] == "2024-01-15"

    def test_empty_dataframe(self):
        wm = datetime(2024, 1, 1, tzinfo=timezone.utc)
        df = pd.DataFrame({"order_date": [], "order_id": []})
        assert len(_filter_since(df, wm)) == 0

    def test_boundary_correct(self):
        wm = datetime(2024, 1, 26, tzinfo=timezone.utc)
        df = self._df(
            ["2024-01-24", "2024-01-25", "2024-01-26", "2024-01-27", "2024-01-28"]
        )
        assert len(_filter_since(df, wm)) == 2


class TestExtractWithWatermark:
    def test_filters_when_since_provided(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(
            textwrap.dedent("""
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-28,South
        """).strip()
        )
        result = extract(csv, since=datetime(2024, 1, 20, tzinfo=timezone.utc))
        assert len(result) == 1
        assert result.iloc[0]["order_id"] == 1002

    def test_returns_all_when_since_is_none(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(
            textwrap.dedent("""
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
            1002,Bob,Mouse,5,29.99,2024-01-28,South
        """).strip()
        )
        assert len(extract(csv, since=None)) == 2

    def test_empty_when_no_rows_pass(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(
            textwrap.dedent("""
            order_id,customer_name,product,quantity,unit_price,order_date,region
            1001,Alice,Laptop,2,999.99,2024-01-15,North
        """).strip()
        )
        assert extract(csv, since=datetime(2024, 6, 1, tzinfo=timezone.utc)).empty


class TestGetWatermark:
    def test_returns_none_on_first_run(self):
        from load import get_watermark

        engine = MagicMock()
        conn = engine.connect.return_value.__enter__.return_value
        conn.execute.return_value.fetchone.return_value = None
        assert get_watermark(engine, pipeline_name="test") is None

    def test_returns_datetime_when_exists(self):
        from load import get_watermark

        engine = MagicMock()
        conn = engine.connect.return_value.__enter__.return_value
        expected = datetime(2024, 1, 27, tzinfo=timezone.utc)
        conn.execute.return_value.fetchone.side_effect = [None, (expected,)]
        assert get_watermark(engine, pipeline_name="test") == expected

    def test_returned_watermark_is_tz_aware(self):
        from load import get_watermark

        engine = MagicMock()
        conn = engine.connect.return_value.__enter__.return_value
        conn.execute.return_value.fetchone.side_effect = [
            None,
            (datetime(2024, 1, 27),),
        ]
        result = get_watermark(engine, pipeline_name="test")
        assert result.tzinfo is not None


class TestSaveWatermark:
    def test_executes_upsert(self):
        from load import save_watermark

        engine = MagicMock()
        conn = engine.begin.return_value.__enter__.return_value
        save_watermark(
            engine, datetime(2024, 1, 27, tzinfo=timezone.utc), pipeline_name="test"
        )
        last_sql = str(conn.execute.call_args_list[-1][0][0])
        assert "ON CONFLICT" in last_sql
        assert "DO UPDATE" in last_sql

    def test_passes_correct_params(self):
        from load import save_watermark

        engine = MagicMock()
        conn = engine.begin.return_value.__enter__.return_value
        wm = datetime(2024, 1, 27, tzinfo=timezone.utc)
        save_watermark(engine, wm, pipeline_name="my_pipeline")
        params = conn.execute.call_args_list[-1][0][1]
        assert params["name"] == "my_pipeline"
        assert params["watermark"] == wm


class TestConstants:
    def test_watermark_column(self):
        assert WATERMARK_COLUMN == "order_date"

    def test_pipeline_name_set(self):
        assert isinstance(PIPELINE_NAME, str) and len(PIPELINE_NAME) > 0

from operators.crawler.cases import *
from operators.crawler.cases.chart_schedule_1 import ChartSchedule_1
from operators.crawler.cases.chart_schedule_2 import ChartSchedule_2
from operators.crawler.cases.chart_schedule_3 import ChartSchedule_3
from operators.crawler.cases.ohlc_schedule_1 import OhlcSchedule_1
from operators.crawler.cases.ohlc_schedule_2 import OhlcSchedule_2
from operators.crawler.cases.ohlc_schedule_3 import OhlcSchedule_3
from operators.crawler.cases.quote_schedule_1 import QuoteSchedule_1
from operators.crawler.cases.tick_schedule_1 import TickSchedule_1
from operators.crawler.cases.tick_schedule_2 import TickSchedule_2

StockTestcaseClasses = {
    'TESTCASE_0': ExampleTestcase,
    'CRAWLER_QUOTEDETAIL_1' : QuoteSchedule_1, #行情快照
    'CRAWLER_CHARTV2TEST_1' : ChartSchedule_1, #走势数据
    'CRAWLER_CHARTV2TEST_2' : ChartSchedule_2,
    'CRAWLER_CHARTV2TEST_3' : ChartSchedule_3,
    'CRAWLER_OHLCV3_1' : OhlcSchedule_1, #历史数据
    'CRAWLER_OHLCV3_2' : OhlcSchedule_2,
    'CRAWLER_OHLCV3_3' : OhlcSchedule_3,
    'CRAWLER_TICK_1' : TickSchedule_1, #分时明细
    'CRAWLER_TICK_2' : TickSchedule_2
}

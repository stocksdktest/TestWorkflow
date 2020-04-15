from operators.crawler.cases import *
from operators.crawler.cases.chart_schedule_1 import ChartSchedule_1
# from operators.crawler.cases.chart_schedule_2 import ChartSchedule_2
from operators.crawler.cases.ohlc_schedule_1 import OhlcSchedule_1
from operators.crawler.cases.ohlc_schedule_2 import OhlcSchedule_2
from operators.crawler.cases.ohlc_schedule_3 import OhlcSchedule_3
from operators.crawler.cases.quote_schedule_1 import QuoteSchedule_1
from operators.crawler.cases.tick_schedule_1 import TickSchedule_1
from operators.crawler.cases.tick_schedule_2 import TickSchedule_2

StockTestcaseClasses = {
    'TESTCASE_0': ExampleTestcase,
    'QUOTEDETAIL_1' : QuoteSchedule_1,
    'CHARTV2TEST_1' : ChartSchedule_1,
    # 'CHARTV2TEST_2' : ChartSchedule_2,
    'OHLCV3_1' : OhlcSchedule_1,
    'OHLCV3_2' : OhlcSchedule_2,
    'OHLCV3_3' : OhlcSchedule_3,
    'TICK_1' : TickSchedule_1,
    'TICK_2' : TickSchedule_2
}

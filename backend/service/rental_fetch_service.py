from scrapers.funda import fundascraper
from scrapers.huislijn import huislijnscraper
from scrapers.huurstunt import huurstuntscraper
from database.databaseConnection import sessionLocal
from scheduler.scheduler import sched


async def FetchFundaRentalObjects():
    
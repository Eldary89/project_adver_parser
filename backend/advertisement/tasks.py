import logging

from celery import shared_task

from .generators.avito_scraper import AvitoScraper

logger = logging.getLogger()


@shared_task
def avito_scrape_data(url):
    scraper = AvitoScraper()
    advertisements = scraper.write_data_to_models(url)
    logging.info(f"{len(advertisements)} got added")

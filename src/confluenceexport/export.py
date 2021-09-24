#! python3

"""
Extract pages from Confluence.
"""

from enum import Enum, unique
import logging
import tempfile

from PyPDF2.merger import PdfFileMerger
from PyPDF2.pdf import PdfFileReader
from .config import Config
from .confluenceclient import ConfluenceClient


#: Create logger for this file.
logger = logging.getLogger()


@unique
class ExportFormat(Enum):
    """
    This class is used to enumerate all format used to export pages.
    """

    #: Pdf extractor
    PDF = "Pdf"

    #: Word extractor
    WORD = "Word"


class ExportEngine:
    """
    This class is used to export pages from Confluence.
    """

    def __init__(self, confluence_client: ConfluenceClient, config: Config):
        """
        Constructs the exporter object.

        :param confluence_client: Confluence client.
        :param config: Configuration to retrieve pages to export.
        """
        logger.debug("Create exporter")

        #: Confluence client
        self._confluence_client: ConfluenceClient = confluence_client

        #: Config
        self._config: Config = config

        logger.debug("Exporter created")

    def export(self) -> None:
        """
        Export the list of given page in Word.
        """


class PdfExport(ExportEngine):
    """
    This class is used to export pages from Confluence in XML format.
    """

    def __init__(
        self,
        confluence_client: ConfluenceClient,
        config: Config,
        filename_destination: str,
    ):
        """
        Constructs the exporter object.

        :param confluence_client: Confluence client.
        :param config: Configuration to retrieve pages to export.
        :param filename_destination: Output Pdf filename.
        """
        logger.debug("Create Pdf exporter")

        super().__init__(confluence_client, config)

        #: Output Pdf filename.
        self._filename_destination: str = filename_destination

        logger.debug("Pdf exporter created")

    def export(self) -> None:
        """
        Export the list of given page in PDF inside one Pdf.
        """
        logger.info("Start Confluence pages export in Pdf format")

        merger = PdfFileMerger()
        for space, titles in self._config.pages_to_export.items():
            for title in titles:
                documentation = self._confluence_client.export_page_in_pdf(
                    space, title
                )
                with tempfile.TemporaryFile() as documentation_file:
                    documentation_file.write(documentation)
                    merger.append(PdfFileReader(documentation_file))
        merger.write(self._filename_destination)
        merger.close()

        logger.info("Confluence pages has been exported in Pdf format")


class WordExport(ExportEngine):
    """
    This class is used to export pages from Confluence in Word format.
    """

    def __init__(
        self,
        confluence_client: ConfluenceClient,
        config: Config,
        filename_destination: str,
    ):
        """
        Constructs the exporter object.

        :param confluence_client: Confluence client.
        :param config: Configuration to retrieve pages to export.
        :param filename_destination: Output Word filename.
        """
        logger.debug("Create Word exporter")

        super().__init__(confluence_client, config)

        #: Output word filename.
        self._filename_destination: str = filename_destination

        logger.debug("Word exporter created")

    def export(self) -> None:
        """
        Export the list of given page in Word.
        """
        logger.info("Start Confluence pages export in Word format")

        for space, titles in self._config.pages_to_export.items():
            for title in titles:
                documentation = self._confluence_client.export_page_in_word(
                    space, title
                )
                with tempfile.TemporaryFile() as documentation_file:
                    documentation_file.write(documentation)

        logger.info("Confluence pages has been exported in Word format")


def _create_export_engine(
    confluence_client: ConfluenceClient,
    config: Config,
) -> ExportEngine:
    """
    Create the export engine depending of the format configured by the
    `config`.

    :param confluence_client: Confluence client to retrieve pages.
    :param config: Configuration to retrieve export format.
    :return: New extractor engine created.
    """
    # Must be integrated in Config
    chart_engine = ExportFormat.PDF
    filename_destination = "Documentation.pdf"

    if chart_engine == ExportFormat.PDF:
        return PdfExport(confluence_client, config, filename_destination)
    if chart_engine == ExportFormat.WORD:
        return WordExport(confluence_client, config, filename_destination)
    raise Exception("Invalid export format")


def export_all_pages(
    confluence_client: ConfluenceClient,
    config: Config,
) -> None:
    """
    Export all pages from Confluence.

    :param confluence_client: Confluence client to get pages.
    :param config: Global configuration.
    """
    logger.info("Export pages from Confluence")

    exporter = _create_export_engine(confluence_client, config)
    exporter.export()

    logger.info("Pages from Confluence exported")

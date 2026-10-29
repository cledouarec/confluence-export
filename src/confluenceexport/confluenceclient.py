"""Client to communicate with Confluence."""

import logging

from atlassian import Confluence

from .errors import ConfluenceExportError

#: Create logger for this file.
logger = logging.getLogger()


class ConfluenceClient:
    """This class is used to interfacing Confluence server."""

    def __init__(
        self,
        confluence_url: str,
        confluence_username: str,
        confluence_password: str,
    ) -> None:
        """Constructs the Confluence client.

        Args:
            confluence_url: URL to connect to Confluence.
            confluence_username: Username to connect to Confluence.
            confluence_password: Password to connect to Confluence.

        Raises:
            ConfluenceExportError: If URL, username or password are invalids.
        """
        logger.debug("Create Confluence client")

        if not confluence_url:
            msg = "Confluence URL is invalid"
            raise ConfluenceExportError(msg)
        if not confluence_username:
            msg = "Confluence username is invalid"
            raise ConfluenceExportError(msg)
        if not confluence_password:
            msg = "Confluence password is invalid"
            raise ConfluenceExportError(msg)
        try:
            # Fix API version for cloud to avoid issue
            if (
                "atlassian.net" in confluence_url
                or "jira.com" in confluence_url
            ):
                api_version = "cloud"
            else:
                api_version = "latest"

            self.__confluence_client: Confluence = Confluence(
                url=confluence_url,
                username=confluence_username,
                password=confluence_password,
                api_version=api_version,
            )
        except Exception as error:
            msg = "Failed to create Confluence client"
            raise ConfluenceExportError(msg) from error

        logger.debug("Confluence client created")

    def create_new_page(
        self,
        space: str,
        parent_page: str,
        title: str,
        message: str,
    ) -> None:
        """Add new page in Confluence in the given `space`.

        The new page will be located under the `parent_page` and will have the
        given `title` and content `message` in Wiki markup format.

        Args:
            space: Confluence space.
            parent_page: Name of the parent page.
            title: Page title.
            message: Page message.

        Raises:
            ConfluenceExportError: If parent page is not found.
        """
        logger.debug("Create new page")

        if not self.__confluence_client.page_exists(space, parent_page):
            msg = "Parent page not found"
            raise ConfluenceExportError(msg)
        parent_id = self.__confluence_client.get_page_id(space, parent_page)

        self.__confluence_client.update_or_create(
            parent_id, title, message, representation="wiki"
        )

        logger.debug("New page created")

    def export_page_in_pdf(self, space: str, title: str) -> str:
        """Export page from Confluence in Pdf.

        Args:
            space: Confluence space.
            title: Page title.

        Returns:
            Page content in Pdf format.

        Raises:
            ConfluenceExportError: If page is not found.
        """
        logger.debug("Export page in Pdf")

        try:
            page_id = self.__confluence_client.get_page_id(space, title)
            page = self.__confluence_client.get_page_as_pdf(page_id)
        except Exception as error:
            msg = "Failed to export Confluence page in Pdf"
            raise ConfluenceExportError(msg) from error

        logger.debug("Page exported in Pdf")
        return page

    def export_page_in_word(self, space: str, title: str) -> str:
        """Export page from Confluence in Word.

        Args:
            space: Confluence space.
            title: Page title.

        Returns:
            Page content in Word format.

        Raises:
            ConfluenceExportError: If page is not found.
        """
        logger.debug("Export page in Word")

        try:
            page_id = self.__confluence_client.get_page_id(space, title)
            page = self.__confluence_client.get_page_as_word(page_id)
        except Exception as error:
            msg = "Failed to export Confluence page in Word"
            raise ConfluenceExportError(msg) from error

        logger.debug("Page exported in Word")
        return page

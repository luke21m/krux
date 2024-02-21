import pytest
from unittest.mock import patch
from ..shared_mocks import mock_context


SEEDS_JSON = """{
    "ecbID": {
        "version": 0,
        "key_iterations": 100000,
        "data": "sMCvAUvVpGSCsXsBl7EBNGPZLymZoyB8eAUHb2TMbarhqD4GJga/SW/AstxIvZz6MR1opXLfF7Pyd+IJBe3E0lDQCkvqytSQfVGnVSeYz+sNfd5T1CXS0/C2zYKTKFL7RTpHd0IXHZ+GQuzX1hoJMHkh0sx0VgorVdDj87ykUQIeC95MS98y/ha2q/vWfLyIZU1hc5VcehzmTA1B6ExMGA=="
    },
    "cbcID": {
        "version": 1,
        "key_iterations": 100000,
        "data": "GpNxj9kzdiTuIf1UYC6R0FHoUokBhiNLkxWgSOHBhmBHb0Ew8wk1M+VlsR4v/koCfSGOTkgjFshC36+n7mx0W0PI6NizAoPClO8DUVamd5hS6irS+Lfff0//VJWK1BcdvOJjzYw8TBiVaL1swAEEySjn5GsqF1RaJXzAMMgu03Kq32iDIDy7h/jHJTiIPCoVQAle/C9vXq2HQeVx43c0LhGXTZmIhhkHPMgDzFTsMGM="
    }
}"""

CBC_ONLY_JSON = """{"cbcID": {"version": 1, "key_iterations": 100000, "data": "GpNxj9kzdiTuIf1UYC6R0FHoUokBhiNLkxWgSOHBhmBHb0Ew8wk1M+VlsR4v/koCfSGOTkgjFshC36+n7mx0W0PI6NizAoPClO8DUVamd5hS6irS+Lfff0//VJWK1BcdvOJjzYw8TBiVaL1swAEEySjn5GsqF1RaJXzAMMgu03Kq32iDIDy7h/jHJTiIPCoVQAle/C9vXq2HQeVx43c0LhGXTZmIhhkHPMgDzFTsMGM="}}"""


@pytest.fixture
def mock_file_operations(mocker):
    mocker.patch(
        "os.listdir",
        new=mocker.MagicMock(return_value=["somefile", "otherfile"]),
    )
    mocker.patch("builtins.open", mocker.mock_open(read_data=SEEDS_JSON))


def test_tools_menu(m5stickv, mocker):
    from krux.pages.tools import Tools
    from krux.pages import MENU_EXIT
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave tools menu
    ]

    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    while True:
        if Tools(ctx).run() == MENU_EXIT:
            break
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)


def test_delete_mnemonic_from_flash(m5stickv, mocker):
    from krux.pages.tools import Tools
    from krux.input import BUTTON_ENTER, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_ENTER,  # Select first mnemonic
        BUTTON_ENTER,  # Confirm deletion
        BUTTON_ENTER,  # Read remove message
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    with patch("krux.encryption.open", new=mocker.mock_open(read_data=SEEDS_JSON)) as m:
        tool = Tools(ctx)
        tool.del_stored_mnemonic()
    # First mnemonic in the list (ECB) will be deleted
    # Assert only CBC remains
    m().write.assert_called_once_with(CBC_ONLY_JSON)


def test_sd_check_no_sd(m5stickv, mocker):
    from krux.pages.tools import Tools
    from krux.input import BUTTON_PAGE
    from unittest.mock import ANY

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Leave
    ]
    mocker.patch(
        "uos.statvfs",
        new=mocker.MagicMock(return_value=[0, 4096, 4096, 0, 1024]),
    )
    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    tool = Tools(ctx)
    tool.flash_text = mocker.MagicMock()
    tool.sd_check()
    tool.flash_text.assert_has_calls([mocker.call("SD card not detected", ANY)])


def test_sd_check(m5stickv, mocker, mock_file_operations):
    from krux.pages.tools import Tools
    from krux.input import BUTTON_PAGE

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Leave
    ]
    mocker.patch(
        "uos.statvfs",
        new=mocker.MagicMock(return_value=[0, 4096, 4096, 0, 1024]),
    )
    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    tool = Tools(ctx)
    tool.sd_check()
    ctx.display.draw_hcentered_text.assert_has_calls(
        [mocker.call("SD card\n\nSize: 16 MB\n\nUsed: 12 MB\n\nFree: 4 MB")]
    )


def test_delete_mnemonic_from_sd(m5stickv, mocker, mock_file_operations):
    from krux.pages.tools import Tools
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    # File reading mock operations will mock 4 mnemonics, 2 from flash, 2 from SD card

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Move to 3rd mnemonic (first listed from SD card)
        BUTTON_PAGE,
        BUTTON_ENTER,  # Select first mnemonic
        BUTTON_ENTER,  # Confirm deletion
        BUTTON_ENTER,  # Read remove message
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    with patch("krux.sd_card.open", new=mocker.mock_open(read_data=SEEDS_JSON)) as m:
        tool = Tools(ctx)
        tool.del_stored_mnemonic()
    # First mnemonic in the list (ECB) will be deleted
    # Assert only CBC remains
    padding_size = len(SEEDS_JSON) - len(CBC_ONLY_JSON)
    m().write.assert_called_once_with(CBC_ONLY_JSON + " " * padding_size)


def test_wipe_device(amigo_tft, mocker):
    """Test that the device is wiped when the user confirms the wipe."""
    from krux.pages.tools import Tools
    from krux.input import BUTTON_ENTER

    BTN_SEQUENCE = [BUTTON_ENTER]  # Confirm wipe

    mocker.spy(Tools, "erase_spiffs")
    ctx = mock_context(mocker)
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
    test_tools = Tools(ctx)
    test_tools.wipe_device()

    assert test_tools.erase_spiffs.call_count == 1


def test_printer_test_tool(amigo_tft, mocker):
    """Test that the print tool is called with the correct text"""
    from krux.pages.tools import Tools
    from krux.themes import theme
    from krux.input import BUTTON_ENTER, BUTTON_PAGE

    BTN_SEQUENCE = [BUTTON_ENTER]  # Confirm print, then leave

    with patch("krux.pages.print_page.PrintPage.print_qr") as mocked_print_qr:
        ctx = mock_context(mocker)
        ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
        test_tools = Tools(ctx)
        test_tools.print_test()

        mocked_print_qr.assert_called_with(
            "Krux Printer Test QR", title="Krux Printer Test QR"
        )


def test_create_qr(amigo_tft, mocker):
    """Test that QR creation tool is called with the correct text"""
    from krux.pages.tools import Tools
    from krux.input import BUTTON_ENTER, BUTTON_PAGE

    BTN_SEQUENCE = [BUTTON_ENTER]

    with patch("krux.pages.qr_view.SeedQRView") as Mocked_QRView:
        ctx = mock_context(mocker)
        ctx.input.wait_for_button = mocker.MagicMock(side_effect=BTN_SEQUENCE)
        test_tools = Tools(ctx)
        test_tools.capture_from_keypad = mocker.MagicMock(return_value="test")
        test_tools.create_qr()

        Mocked_QRView.assert_called_with(ctx, data="test", title="Custom QR Code")

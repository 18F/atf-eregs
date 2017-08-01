from unittest.mock import Mock, call

from django.core.management import call_command

from atf_eregs.management.commands import fetch_atf_resources


def test_run_once(monkeypatch):
    """If given no parameters, we will run the fetch once."""
    monkeypatch.setattr(fetch_atf_resources, 'fetch_and_save_resources',
                        Mock())

    call_command('fetch_atf_resources')

    assert fetch_atf_resources.fetch_and_save_resources.called


def test_run_indefinitely(monkeypatch):
    """If given a specific period, we should run on that periodic basis."""
    monkeypatch.setattr(fetch_atf_resources, 'fetch_and_save_resources',
                        Mock())
    monkeypatch.setattr(fetch_atf_resources, 'time', Mock())
    monkeypatch.setattr(fetch_atf_resources, 'infinite_loop', Mock())
    # set up for three runs
    fetch_atf_resources.infinite_loop.side_effect = [True, True, True, False]
    # time() is called twice per run
    fetch_atf_resources.time.time.side_effect = [
        1000, 1005,  # took 5 seconds to run
        1100, 1305,  # took 205 second to run
        1305, 1310,  # took 5 seconds to run
    ]

    call_command('fetch_atf_resources', '--period', '100')

    assert fetch_atf_resources.fetch_and_save_resources.call_count == 3
    assert fetch_atf_resources.time.sleep.call_args_list == [
        call(95),   # 5 seconds to run, sleep the remaining 95
        call(0),    # ran too long, don't sleep at all
        call(95),   # 5 seconds again; sleep the remaining 95
    ]


def test_exception(monkeypatch):
    """Exceptions raised by requests won't kill the process."""
    monkeypatch.setattr(fetch_atf_resources, 'fetch_and_save_resources',
                        Mock())
    monkeypatch.setattr(fetch_atf_resources, 'infinite_loop', Mock())
    # set up for three runs
    fetch_atf_resources.fetch_and_save_resources.side_effect = IOError
    fetch_atf_resources.infinite_loop.side_effect = [True, True, True, False]

    call_command('fetch_atf_resources', '--period', '0')

    assert fetch_atf_resources.fetch_and_save_resources.call_count == 3

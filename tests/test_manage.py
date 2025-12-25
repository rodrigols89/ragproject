"""Tests for manage.py."""
import os
import sys

# Import manage module - pytest-django handles Django setup
import manage

main = manage.main


def test_main_sets_django_settings_module_when_not_set(monkeypatch):
    """Test that main() sets DJANGO_SETTINGS_MODULE when not defined."""
    called_args = []

    def mock_execute(args):
        called_args.append(args)

    # Remove DJANGO_SETTINGS_MODULE if it exists
    monkeypatch.delenv('DJANGO_SETTINGS_MODULE', raising=False)
    monkeypatch.setattr(manage, 'execute_from_command_line', mock_execute)
    monkeypatch.setattr(sys, 'argv', ['manage.py', 'help'])

    main()

    # Verify DJANGO_SETTINGS_MODULE was set
    assert os.environ.get('DJANGO_SETTINGS_MODULE') == 'core.settings'

    # Verify execute_from_command_line was called
    assert called_args == [['manage.py', 'help']]


def test_main_preserves_existing_django_settings_module(monkeypatch):
    """Test that main() preserves DJANGO_SETTINGS_MODULE if already set."""
    original_value = 'custom.settings'
    called_args = []

    def mock_execute(args):
        called_args.append(args)

    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', original_value)
    monkeypatch.setattr(manage, 'execute_from_command_line', mock_execute)
    monkeypatch.setattr(sys, 'argv', ['manage.py', 'help'])

    main()

    # Verify DJANGO_SETTINGS_MODULE was preserved
    assert os.environ.get('DJANGO_SETTINGS_MODULE') == original_value

    # Verify execute_from_command_line was called
    assert called_args == [['manage.py', 'help']]


def test_main_calls_execute_from_command_line_with_sys_argv(monkeypatch):
    """Test that main() calls execute_from_command_line with sys.argv."""
    test_argv = ['manage.py', 'migrate', '--noinput']
    called_args = []

    def mock_execute(args):
        called_args.append(args)

    monkeypatch.delenv('DJANGO_SETTINGS_MODULE', raising=False)
    monkeypatch.setattr(manage, 'execute_from_command_line', mock_execute)
    monkeypatch.setattr(sys, 'argv', test_argv)

    main()

    # Verify execute_from_command_line was called with correct args
    assert called_args == [test_argv]


def test_main_handles_different_commands(monkeypatch):
    """Test that main() works with different Django management commands."""
    commands = [
        ['manage.py', 'runserver'],
        ['manage.py', 'migrate'],
        ['manage.py', 'collectstatic', '--noinput'],
        ['manage.py', 'shell'],
    ]

    monkeypatch.delenv('DJANGO_SETTINGS_MODULE', raising=False)

    for command in commands:
        called_args = []

        def mock_execute(args):
            called_args.append(args)

        monkeypatch.setattr(manage, 'execute_from_command_line', mock_execute)
        monkeypatch.setattr(sys, 'argv', command)

        main()

        # Verify execute_from_command_line was called correctly
        assert called_args == [command]

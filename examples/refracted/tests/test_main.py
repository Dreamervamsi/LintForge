from refracted import main


def test_main_output(capsys):
    """Test that main function prints expected output."""
    main()
    captured = capsys.readouterr()
    assert "Hello from refracted!" in captured.out

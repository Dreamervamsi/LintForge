from original import main


def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from original!" in captured.out

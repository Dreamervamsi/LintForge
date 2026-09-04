from refracted import main


def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from refracted!" in captured.out

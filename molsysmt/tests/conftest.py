def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    import molsysmt as msm
    msm.tools.nglview.adding_molsysmt()


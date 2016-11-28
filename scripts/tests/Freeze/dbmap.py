# **********************************************************************
#
# Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

class FreezeDBMapTestCase(ClientTestCase):

    def setupClientSide(self, current):
        self.mkdirs("db")

TestSuite(__name__, [FreezeDBMapTestCase(client=SimpleClient(props={ "Freeze.Warn.Rollback" : 0 }, args=["{testdir}"]))])
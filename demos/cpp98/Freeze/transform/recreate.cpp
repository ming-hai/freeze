// **********************************************************************
//
// Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
//
// **********************************************************************

#include <Ice/Ice.h>
#include <Freeze/Freeze.h>
#include <NewContacts.h>

using namespace std;
using namespace Demo;
using namespace Freeze;

class Recreate : public Ice::Application
{
public:

    virtual int run(int, char*[]);
};

int main(int argc, char* argv[])
{
    Recreate app;
    return app.main(argc, argv);
}

int
Recreate::run(int, char*[])
{
    ConnectionPtr connection = createConnection(communicator(), "dbnew");
    NewContacts::recreate(connection, "contacts");

    cout << "Recreated contacts database successfully!" << endl;
    return 0;
}

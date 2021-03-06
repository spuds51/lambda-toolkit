import getopt
from help import Help
from modules.queue import Queue
from modules.project import Project
from modules.ltklambdaproxy import Ltklambdaproxy
from modules.receiver import Receiver
from modules.role import Role

class Gateway:

    projectname = ""
    sqsname = ""
    lambdaname = ""
    rolename = ""

    def __init__(self,action, args):
        self.action = action
        self.get_args(args)


    def get_args(self, args):
        try:
            opts, args = getopt.getopt(args, "p:q:l:r:",
                                       ["projectname=", "sqsname=", "lambdaname=", "rolename="])
        except getopt.GetoptError:
            Help.print_help("Getopterror")
            exit(1)
        for opt, arg in opts:
            if opt in ("-p", "--projectname"):
                self.projectname = arg
            elif opt in ("-q", "--sqsname"):
                if arg.endswith(".fifo"):
                    self.sqsname = arg
                else:
                    self.sqsname = arg + ".fifo"
            elif opt in ("-r", "--rolename"):
                self.rolename = arg
            elif opt in ("-l", "--lambdaname"):
                self.lambdaname = arg

    def do_action(self, conf):
        if self.action == "create-project":
            return Project(conf, self.projectname).create_project()
        elif self.action == "delete-project":
            return Project(conf, self.projectname).delete_project()
        elif self.action == "list":
            conf.list_config()
        elif self.action == "create-sqs":
            return Queue(conf, self.sqsname).create_queue()
        elif self.action == "delete-sqs":
            return Queue(conf, self.sqsname).delete_queue()
        elif self.action == "deploy-project":
            return Project(conf, self.projectname).deploy_project(self.rolename)
        elif self.action == "import-project":
            return Project(conf, self.projectname).import_project()
        elif self.action == "undeploy-project":
            return Project(conf, self.projectname).undeploy_project()
        elif self.action == "deploy-lambda-proxy":
            return Ltklambdaproxy(conf, self.lambdaname).deploy_lambda_proxy(self.rolename, self.sqsname)
        elif self.action == "undeploy-lambda-proxy":
            return Ltklambdaproxy(conf, self.lambdaname).undeploy_lambda_proxy()
        elif self.action == "receiver":
            try:
                Receiver(conf, self.sqsname, self.projectname).receiver()
            except KeyboardInterrupt:
                print("Stopping the receive.")
        elif self.action == "set-default-role":
            Role(conf, self.rolename).set_default_role()
        elif self.action == "create-star":
            conf = Project(conf, self.projectname).create_project()
            conf = Queue(conf, self.projectname + "_queue").create_queue()
            conf = Ltklambdaproxy(conf, self.projectname + "_proxy").deploy_lambda_proxy(self.rolename, self.projectname + "_queue")
            return Project(conf, self.projectname).deploy_project(self.rolename)
        elif self.action == "delete-all-configuration":
            conf.delete_all_config()
        else:
            Help.print_help("Invalid command")

        return conf


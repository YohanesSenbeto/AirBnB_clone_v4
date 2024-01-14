#!/usr/bin/python3
""" console """

import cmd
import shlex
import re
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import models

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')
if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    models.storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    models.storage = FileStorage()

class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class

        Usage: create <Class name> <param 1>=<value 1> <param 2>=<value 2> ...

        Example:
        create BaseModel name="John Doe" age=25
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False
        else:
            kwargs = {}
            for arg in args[1:]:
                match = re.fullmatch('(?P<key>[a-zA-Z_]\w*)=(?:'
                                     '(?P<int>\d+)|'
                                     '(?P<float>\d*\.\d*)|'
                                     '(?P<string>.*))',
                                     arg)
                match = match.groupdict()
                if match['string']:
                    kwargs[match['key']] = match['string'].replace('_', ' ')
                elif match['float']:
                    if match['float'] == '.':
                        continue
                    kwargs[match['key']] = float(match['float'])
                else:
                    kwargs[match['key']] = int(match['int'])

            instance = classes[args[0]](**kwargs)
            try:
                instance.save()
            except Exception as e:
                print("** could not save [{}] object **".format(args[0]))
                print(e)
                return False
            else:
                print(instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance

        Usage: show <Class name> <id>

        Example:
        show BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id

        Usage: destroy <Class name> <id>

        Example:
        destroy BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all()[key].delete()
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances

        Usage: all [Class name]

        Example:
        all
        all BaseModel
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            for value in models.storage.all().values():
                obj_list.append(str(value))
        elif args[0] in classes:
            for key in models.storage.all():
                if key.startswith(args[0]):
                    obj_list.append(str(models.storage.all()[key]))
        else:
            print("** class doesn't exist **")
            return False
        print(obj_list)

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value

        Usage: update <Class name> <id> <attribute name> <new value>

        Example:
        update BaseModel 1234-1234-1234 name "John Doe"
        """
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_help(self, arg):
        """Display help for available commands"""
        commands = [
            'EOF', 'emptyline', 'quit', 'create', 'show', 'destroy', 'all',
            'update', 'count', 'get', 'close'
        ]
        print("Available commands:")
        for cmd in commands:
            print(f"  {cmd}")
        print("\nUsage examples:")
        print("  create BaseModel name=\"John Doe\" age=25")
        print("  show BaseModel 1234-1234-1234")
        print("  destroy BaseModel 1234-1234-1234")
        print("  all")
        print("  all BaseModel")
        print("  update BaseModel 1234-1234-1234 name \"John Doe\"")
        print("  count BaseModel")
        print("  get BaseModel 1234-1234-1234")
        print("  close")

    def do_count(self, arg):
        """Count the number of instances of a class

        Usage: count <Class name>

        Example:
        count BaseModel
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            count = models.storage.count(args[0])
            print(count)
        else:
            print("** class doesn't exist **")

    def do_get(self, arg):
        """Retrieve an instance by ID

        Usage: get <Class name> <id>

        Example:
        get BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        if args[0] in classes:
            obj = models.storage.get(args[0], args[1])
            if obj:
                print(obj)
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_close(self, arg):
        """Close the console"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()

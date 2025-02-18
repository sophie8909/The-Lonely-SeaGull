# =============================================================================
# UndoManager.py
# =============================================================================
# @AUTHOR: Lars Oestreicher
# @VERSION: 2.0
# @DATE: February 14, 2025
#
# =============================================================================
# First we define the main data structure used by the UndoManager, the Stack.
# A stack has a FILO-access order. It is constructed from a list, with
# apropriate accessors added.
#
class Stack :

    # Basically a stack consists of a list.
    #
    st = []

    # Push means to add an object on top of the stack.
    #
    def push(self, obj):
        self.st.append(obj)

    # Pop means to remove (and return) the topmost object on the stack.
    # If it is the last object on the stack, nothing happens.
    #
    def pop(self):
        lastObject = self.st[-1]
        if len(self.st) > 1 :
            self.st = self.st[0:-1]
        else :
            pass

        return lastObject

    # Resetting a stack means to empty it leaving a []
    #
    def reset(self):
        self.st = []


class UndoManager :

    # Set all the initial values in the constructor.
    #
    def __init__(self, ctrl):
        self.controller = ctrl
        self.undoStack = Stack()
        self.redoStack = Stack()

    # The doIt function is the first function to be performed, before the
    # object is put on the UNDO-stack. All the functions in the undo-manager
    # will update the view to show the new state.
    #
    # Note that the execution of any function will also empty the REDO-stack,
    # to keep the consistency of the UNDO-system.
    #
    def doIt(self, funcObject) :
        funcObject.execute()
        self.undoStack.push(funcObject)
        self.redoStack.reset()
        self.controller.update_view()

    # The unDoit function is used for the UNDO. The function object is
    # popped from the UNDO-stack and then the unexecute function of the
    # function object is called, before the object is now pushed onto the
    # REDO-stack.
    #
    def undoIt(self):
        funcObject = self.undoStack.pop()
        funcObject.unexecute()
        self.redoStack.push(funcObject)
        self.controller.update_view()

    # The redoIt function will start by popping the function object
    # from the REDO-stack. The reexecute function is executed, and the
    # function object is pushed back onto the UNDO-stack.
    def redoIt(self):
        funcObject = self.redoStack.pop()
        funcObject.reexecute()
        self.undoStack.push(funcObject)
        self.controller.update_view()

# =============================================================================
# END OF UndoManager.py
# =============================================================================
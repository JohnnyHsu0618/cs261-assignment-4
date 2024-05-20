# Name:CHE-HAN HSU
# OSU Email:hsuche@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:assignment 4
# Due Date: 20,05,2024
# Description:In this program we will be implementing an AVL tree.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        
        new_node = AVLNode(value)           # Create a new node for new data
        if self._root is None:              # If it is an empty tree
            self._root = new_node           # Make the new node the root of the tree.  
            return
        
        current = self._root
        parent = None
        while current:                      # Find insertion point
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent            # Set the parent field of the new node
        if value < parent.value:            # Install a new node
            parent.left = new_node
        else:
            parent.right = new_node

        self._rebalance(new_node)           # Set up the height field of the new node and check for balance.


    def remove(self, value: object) -> bool:
        
        node = self._root
        parent = None
        while node and node.value != value:    # Find the node to be deleted
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right
        
        if node is None:    # No node to delete was found.
            return False

        if node.left is None and node.right is None:                # To delete a node that has no subtree.
            check_bf = self._remove_no_subtrees(parent,node)
        elif node.left is None or node.right is None:               # To delete a node with only one subtree.
            check_bf = self._remove_one_subtree(parent, node)
        else:                                                       # To delete a node that has two subtrees.
            check_bf = self._remove_two_subtrees(parent, node)
        
        self._rebalance(check_bf)   # Check balance
        return True

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_no_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        
        # remove node that has no subtrees (no left or right nodes)
        if remove_parent is None:                   # If the node to be deleted is the root and the root has no subtrees.
            self._root = None                       # After deleting, it becomes an empty tree.
        elif remove_parent.left == remove_node:
            remove_parent.left = None
        else:
            remove_parent.right = None

        return remove_parent

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        
        # remove node that has a left or right subtree (only)
        if remove_node.left:                # The node to be deleted has a unique subtree, and that subtree is the left subtree.
            child = remove_node.left
        else:                               # The node to be deleted has a unique subtree, which is the right subtree.
            child = remove_node.right

        child.parent = remove_parent

        if remove_parent is None:           # If what needs to be removed is the tree root.
            self._root = child              # Make the child the new root of the tree.
        elif remove_parent.left == remove_node:
            remove_parent.left = child
        else:
            remove_parent.right = child

        return remove_parent

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        
        successor_parent = remove_node
        successor = remove_node.right

        while successor.left:                   # Find the minimum value in the right subtree.
            successor_parent = successor
            successor = successor.left

        remove_node.value = successor.value     
        if successor_parent.left == successor:
            if successor.right:
                successor.right.parent = successor_parent   # f the right subtree of the minimum value node is not empty, then the parent field of it should be set.
            successor_parent.left = successor.right
        else:
            if successor.right:
                successor.right.parent = successor_parent   # If the right subtree of the minimum value node is not empty, then its parent field needs to be set.
            successor_parent.right = successor.right        # If the minimum value node is the root of the right subtree.

        return successor_parent

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #

    def _balance_factor(self, node: AVLNode) -> int:
        
        return self._get_height(node.left) - self._get_height(node.right)   # Calculate the balance factor of a node.


    def _get_height(self, node: AVLNode) -> int:
        
        if node is None:        # If the node is empty, the height is -1; if the node is a leaf, the height is 0.
            return -1
        return node.height      # Get the height of a node.


    def _rotate_left(self, node: AVLNode) -> AVLNode:      
        
        new_root = node.right                   # Let new_root be the new root after left rotation.
        node.right = new_root.left              # Clear the left link of new_root.

        # set parent
        if new_root.left:                       
            new_root.left.parent = node         
        new_root.parent = node.parent

        # put down new roots
        if node.parent is None:                 # If node is the root of the tree
            self._root = new_root               # new_root becomes the new root of the entire tree.
        elif node == node.parent.left:          
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        new_root.left = node                    # Attach the node to the left of the new root.
        node.parent = new_root                  # Set parent

        self._update_height(node)               # Update height
        self._update_height(new_root)           
        return new_root                         # new_root adjusted downwards, completed.


    def _rotate_right(self, node: AVLNode) -> AVLNode:      
        
        new_root = node.left                    # Let new_root be the new root after right rotation.
        node.left = new_root.right              # Empty the right link of new_root

        # set parent
        if new_root.right:
            new_root.right.parent = node
        new_root.parent = node.parent

        # put down new roots
        if node.parent is None:                 # If node is the root of the tree
            self._root = new_root               # new_root becomes the new root of the entire tree.
        elif node == node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root

        new_root.right = node               # Attach the node to the right side of the new root.
        node.parent = new_root              # set parent

        self._update_height(node)           # update height
        self._update_height(new_root)
        return new_root                     # The new_root has been adjusted downward, completed.


    def _update_height(self, node: AVLNode) -> None:
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))


    def _rebalance(self, node: AVLNode) -> None:
        
        while node:                                             # Adjust to the top
            self._update_height(node)                           # update height
            balance = self._balance_factor(node)                # check balance
            
            if balance > 1:                                     # The left tree is taller, so we need to perform a right rotation (LL type or LR type).
                if self._balance_factor(node.left) < 0:         # LR type
                    self._rotate_left(node.left)                # First rotate left, then rotate right.
                node = self._rotate_right(node)                 
            elif balance < -1:                                  # The right subtree is taller, requiring a left rotation (RR type or RL type).
                if self._balance_factor(node.right) > 0:        # RL type
                    self._rotate_right(node.right)              # First rotate right, then rotate left.
                node = self._rotate_left(node)
            
            node = node.parent                                  # Continue to adjust upwards.

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

class BookNode:
    def __init__(self, isbn, title, author, genre, price, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.left = None
        self.right = None
        self.height = 1

class BookInventory:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def add_book(self, isbn, title, author, genre, price, quantity):
        def _add_book(node, isbn, title, author, genre, price, quantity):
            if not node:
                return BookNode(isbn, title, author, genre, price, quantity)
            elif isbn < node.isbn:
                node.left = _add_book(node.left, isbn, title, author, genre, price, quantity)
            elif isbn > node.isbn:
                node.right = _add_book(node.right, isbn, title, author, genre, price, quantity)
            else:
                raise ValueError("This ISBN already exists")

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)
            if balance > 1 and isbn < node.left.isbn:
                return self._rotate_right(node)
            if balance < -1 and isbn > node.right.isbn:
                return self._rotate_left(node)
            if balance > 1 and isbn > node.left.isbn:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            if balance < -1 and isbn < node.right.isbn:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
            return node

        self.root = _add_book(self.root, isbn, title, author, genre, price, quantity)

    def remove_book(self, isbn):
        def _remove_book(node, isbn):
            if not node:
                return node
            elif isbn < node.isbn:
                node.left = _remove_book(node.left, isbn)
            elif isbn > node.isbn:
                node.right = _remove_book(node.right, isbn)
            else:
                if not node.left:
                    temp = node.right
                    node = None
                    return temp
                elif not node.right:
                    temp = node.left
                    node = None
                    return temp
                temp = self._min_value_node(node.right)
                node.isbn = temp.isbn
                node.title = temp.title
                node.author = temp.author
                node.genre = temp.genre
                node.price = temp.price
                node.quantity = temp.quantity
                node.right = _remove_book(node.right, temp.isbn)
            if not node:
                return node

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)
            if balance > 1 and self._balance_factor(node.left) >= 0:
                return self._rotate_right(node)
            if balance < -1 and self._balance_factor(node.right) <= 0:
                return self._rotate_left(node)
            if balance > 1 and self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            if balance < -1 and self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
            return node

        self.root = _remove_book(self.root, isbn)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def search_books(self, key, value):
        def _search_books(node, key, value):
            results = []
            if node:
                if key == 'isbn':
                    if node.isbn == value:
                        results.append(node)
                elif key == 'title':
                    if value.lower() in node.title.lower():
                        results.append(node)
                elif key == 'author':
                    if value.lower() in node.author.lower():
                        results.append(node)
                elif key == 'genre':
                    if value.lower() in node.genre.lower():
                        results.append(node)
                results += _search_books(node.left, key, value)
                results += _search_books(node.right, key, value)
            return results

        return _search_books(self.root, key, value)

    def display_inventory(self):
        def _inorder_traversal(node):
            result = []
            if node:
                result += _inorder_traversal(node.left)
                result.append((node.isbn, node.title, node.author, node.genre, node.price, node.quantity))
                result += _inorder_traversal(node.right)
            return result

        return _inorder_traversal(self.root)

    def order_book(self, isbn, quantity):
        book = self.search_books('isbn', isbn)
        if book:
            book = book[0]
            if book.quantity >= quantity:
                book.quantity -= quantity
                return f"Order successfully placed for {quantity} copies of '{book.title}'"
            else:
                return "Sorry, insufficient quantity available for this book"
        else:
            return "Book not found in inventory"

    def restock_inventory(self, isbn, quantity):
        book = self.search_books('isbn', isbn)
        if book:
            book = book[0]
            book.quantity += quantity
            return f"Inventory successfully restocked with {quantity} copies of '{book.title}'"
        else:
            return "Book not found in inventory"

if __name__ == "__main__":
    book_inventory = BookInventory()

    # Adding books
    book_inventory.add_book("9780553106633", "Wimpy kid", "Jeff kinney", "Entertainment", 450, 50)
    book_inventory.add_book("9780061120084", "Alif", "A.Abdaal", "Poetry", 600, 100)
    book_inventory.add_book("9781400079179", "Art of defending", "Alex Ferguson", "Fiction", 1200, 100)

    # Displaying inventory
    print("Total Book Inventory:")
    for book in book_inventory.display_inventory():
        print(book)

    # Searching books
    print("\nSearching for Results:")
    search_results = book_inventory.search_books("author", "George")
    for book in search_results:
        print(book.title, "written by", book.author)

    # Ordering books
    print("\nYour order has been placed for:")
    print(book_inventory.order_book("9781400079179", 20))

    # Restocking inventory
    print("\nRestocking the whole inventory:")
    print(book_inventory.restock_inventory("9781400079179", 47))

    # Displaying updated inventory
    print("\nUpdated Inventory:")
    for book in book_inventory.display_inventory():
        print(book)

import unittest
from server import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.server = 'test_server'
        self.username = 'test_user'
        self.message = 'test_message'

    def test_add_message(self):
        self.db.add_message(self.server, self.username, self.message)
        # Check if the message was added to the database
        self.db.cursor.execute('''
            SELECT *
            FROM messages
            WHERE server = ? AND username = ? AND message = ?
        ''', (self.server, self.username, self.message))
        self.assertEqual(len(self.db.cursor.fetchall()), 1)

    def test_get_last_messages(self):
        self.db.add_message(self.server, self.username, self.message)
        messages = self.db.get_last_messages(self.server)
        # Check if the correct number of messages is returned
        self.assertEqual(len(messages), 1)
        # Check if the returned message is the one we added
        self.assertEqual(messages[0][2], self.username)
        self.assertEqual(messages[0][3], self.message)

    def test_get_messages_before(self):
        self.db.add_message(self.server, self.username, self.message)
        message_id = self.db.cursor.lastrowid
        messages = self.db.get_messages_before(self.server, message_id)
        # Check if no messages are returned
        self.assertEqual(len(messages), 0)
        
    def tearDown(self):
        # Delete all test data from the messages table
        self.db.cursor.execute('''
            DELETE FROM messages
            WHERE server = ? AND username = ? AND message = ?
        ''', (self.server, self.username, self.message))
        self.db.conn.commit()

if __name__ == '__main__':
    unittest.main()
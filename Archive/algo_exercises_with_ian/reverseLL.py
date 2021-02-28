def revLL(head):
    cursor = head
    while cursor is not None:
        cursor.prev, cursor.next = cursor.next, cursor.prev
        cursor = cursor.prev
    return cursor.next

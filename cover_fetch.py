def get_cover(isbn):
    # This function creates the cover image for the book using the isbn
    image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    return image_url

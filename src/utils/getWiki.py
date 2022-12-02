import wikipedia


def getEmbedImage(images, term, title):
    link = None
    words = term.split(' ')
    words2 = title.split(' ')
    for url in images:
        if ("cover" in url):
            link = url
            break
        if ("poster" in url):
            link = url
            break
        for word in words:
            if (len(word) >= 4):
                if (word in url):
                    link = url
                    break
        for word in words2:
            if (len(word) >= 4):
                if (word in url):
                    link = url
                    break
    return link


def getWiki(term, sentences, language='en'):
    wikipedia.set_lang(language)
    try:
        page = wikipedia.page(term)
    except Exception as e:
        e
        page = None

    if (page is None):
        wikipedia.set_lang('pt')
        try:
            page = wikipedia.page(term)
        except Exception as e:
            e
            return (-1, -1, -1)

    content = wikipedia.summary(term, sentences=sentences)
    link = getEmbedImage(page.images, term, page.title)

    return (content, link, page)


def getWikiSimple(term, sentences):
    wikipedia.set_lang('simple')
    try:
        page = wikipedia.page(term)
    except Exception as e:
        e
        return (-1, -1, -1)

    content = wikipedia.summary(term, sentences=sentences)
    link = getEmbedImage(page.images, term, page.title)
    return (content, link, page)

# import requests
from bs4 import BeautifulSoup
# from mdutils.mdutils import MdUtils
import os

sample_data = {
    'name':
    'Testing Product',
    'details': [{
        'key': 'key',
        'value': 'value'
    }, {
        'key': 'key',
        'value': 'value'
    }, {
        'key': 'key',
        'value': 'value'
    }],
    'description':
    '  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Senectus et netus et malesuada fames. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum.',
    'manufacturing_details':
    '    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Senectus et netus et malesuada fames. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum.',
    'thumbnail':
    'https://ucarecdn.com/236d7a9c-dc2d-4878-a072-9e5ee29ad9d7/',
    'category':
    'essential oil'
}


def scrapeProductsFromCategoryPage(category):
    # os.mkdir(category) # for storing files under category folder
    file_name = category + '.html'
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html5lib')
    products = soup.find_all('div', class_="prdCard")

    # scraping data for a single product
    for product in products:
        data = {
            'name': '',
            'details': [],  # arr of object with key value pair
            'category': category.replace('-', ' '),
            'thumbnail': ''
        }
        data['name'] = product.select('h2 > div')[0].get_text()
        data['thumbnail'] = product.find('img').attrs['dataimg']

        # populating details in key value format
        for product_attr in product.find_all('tr'):
            detail = {'key': '', 'value': ''}
            detail['key'], detail['value'] = [
                x.get_text() for x in product_attr.find_all('td')
            ]
            data['details'].append(detail)
        createProductMarkdownFile(data, category)
    # print(data)
    # os.mkdir(category)
    # for prd in products:
    #     productName = prd.select('h2 > div')[0].get_text()

    # createFile(productName, file)


def scrapeAllData():
    files = os.listdir('./')
    htmlFiles = [file for file in files if file.endswith('.html')]
    [
        scrapeProductsFromCategoryPage(file.replace('.html', ''))
        for file in htmlFiles
    ]

# creating proper markdown for each detail key
def insertDetail(obj, file):
    file.write('  - detail:\n')
    file.write('      key: "' + obj['key'] + '"\n')
    file.write('      value: "' + obj['value'] + '"\n')


# function for creating a markdown file using details
def createProductMarkdownFile(details, directory):
    # mdFile = open('./' + directory + '/' + details['name'] + ".md", "w+")
    mdFile = open('./all/' + details['name'] + ".md", "w+")
    mdFile.write('---\n')
    # inserting name and title
    mdFile.write('name: ' + details['name'] + '\n')
    mdFile.write('title: ' + details['name'] + '\n')

    # inserting details of product
    mdFile.write('details:\n')
    # iterate through the key value pair here
    for detail in details['details']:
        insertDetail(detail, mdFile)

    # inserting description
    if 'description' in details:
        mdFile.write('description: >-\n')
        mdFile.write(details['description'])
        mdFile.write('\n')

    # iserting manufacturing details
    if 'manufacturing_details' in details:
        mdFile.write('manufacturing_details:\n')
        mdFile.write('  - >-\n')
        mdFile.write(details['manufacturing_details'])
        mdFile.write('\n')

    # inserting showOnHomeKey
    mdFile.write('showOnHome: false\n')

    # inserting thumbnail
    mdFile.write('thumbnail: ' + details['thumbnail'] + "\n")

    # inserting product images
    mdFile.write('productImages:\n')
    mdFile.write(
        '  - https://ucarecdn.com/8213c725-21d0-4ac0-ad5e-c1975c20032b/\n')

    # inserting category
    mdFile.write('category: ' + details['category'] + '\n')
    mdFile.write('---')
    mdFile.close()


# deletes markdown files in the root directory
def deleteMarkdownFiles(dir):
    files = os.listdir('./' + dir)
    print(files)
    mdFiles = [file for file in files if file.endswith('.md')]
    for file in mdFiles:
        os.remove('./' + dir + '/' + file)


deleteMarkdownFiles('all')

# createFile(sample_data,'testing')

# scrapeCategoryData()

# scrapeProductsFromCategory('essential-oils')
scrapeAllData()
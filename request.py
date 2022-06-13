import requests
import pandas as pd
from lxml import html


def send_request(url):
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'your_api_key',
            'url': url,
        },

    )
    return response.content


old_data = pd.read_csv("old_data.csv")
search_list = old_data['part_number'].tolist()
manufact = old_data['manufacturer'].tolist()
data = {
    'part_number': old_data['part_number'].tolist()[0:12],
    'manufacturer': old_data['manufacturer'].tolist()[0:12],
    'Scraped Part': [' ', '15-24-7161', '22-05-7065', '22-12-2024', '22-17-3082', '22-27-2041', '7010326660',
                     '22-28-0031', '22-28-4020', '39-28-1083', '39-29-9042', '30700-1147'],
    'Also known as': [' ', '15247161', ' ', '22122024', ' ', ' ', ' ', '22280031', '22284020', '39281083', '39299042',
                      '307001147'],
    'Median Price': [' ', 'USD 2.470', 'USD 0.193', 'USD 0.240', 'USD 0.860', 'USD 0.193', 'USD 1.614', 'USD 0.299',
                     'USD 0.046', 'USD 0.463', 'USD 0.330', 'USD 1.300'],
    'Match': ['FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE']
}
j = 0
for i in search_list[12::]:
    tree = html.fromstring(send_request(f'https://octopart.com/search?q={i}'))
    button = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/span')
    if not button:
        scraped_part = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/'
                                  'div[1]/div[1]/div/a/div[2]/span/span')
        if scraped_part:
            scraped_part = scraped_part[0].text
        else:
            scraped_part = ' '
        amount = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/'
                            'div[1]/div[1]/div/div/span[2]')
        if amount:
            amount = amount[0].text
            currency = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/'
                                  'div[2]/div[1]/div[1]/div/div/span[1]')[0].text
            price = f'{currency} {amount}'
        else:
            price = ' '

        aka = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[2]/mark')
        if not aka:
            aka = ' '
        else:
            aka = aka[0].text
        data['part_number'].append(i)
        data['manufacturer'].append(manufact[search_list.index(i)])
        data['Scraped Part'].append(scraped_part)
        data['Also known as'].append(aka)
        data['Median Price'].append(price)
        data['Match'].append(' ')
        df = pd.DataFrame(data)

        writer = pd.ExcelWriter('new_data.xlsx', engine='xlsxwriter')

        df.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.save()
        j += 1
        print(j)
    else:
        scraped_part = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/'
                                  'div/div[1]/div[1]/div/a/div[2]/span/span')
        if scraped_part:
            scraped_part = scraped_part[0].text
        else:
            scraped_part = ' '
        amount = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/div[2]/'
                            'div[1]/div[1]/div/div/span[2]')
        if amount:
            amount = amount[0].text
            currency = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/'
                                  'div[2]/div[1]/div[1]/div/div/span[1]')[0].text
            price = f'{currency} {amount}'
        else:
            price = ' '

        aka = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[2]/mark')
        if not aka:
            aka = ' '
        else:
            aka = aka[0].text
        data['part_number'].append(i)
        data['manufacturer'].append(manufact[search_list.index(i)])
        data['Scraped Part'].append(scraped_part)
        data['Also known as'].append(aka)
        data['Median Price'].append(price)
        data['Match'].append('Not Found')
        df = pd.DataFrame(data)

        writer = pd.ExcelWriter('new_data.xlsx', engine='xlsxwriter')

        df.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.save()
        print('not found')

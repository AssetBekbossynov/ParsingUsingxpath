from lxml import html
import requests


if __name__ == '__main__':

    page = requests.get('https://freelansim.ru/tasks?categories=development_android')
    tree = html.fromstring(page.content)

    taskLink = tree.xpath('/html/body/div[2]/main/section/div/div/div/ul/li/article/div/header/div[1]/a/@href')

    file = open("testfile.txt", "a+")
    file.seek(0)
    lastLink = file.readline()[:-1]

    for link in taskLink:
        if(str(lastLink) != str(link)):
            singlePage = requests.get('https://freelansim.ru' + link)
            singlePageTree = html.fromstring(singlePage.content)

            taskTitle = (singlePageTree.xpath('/html/body/div[2]/main/section/div/div/div/div[1]/h2/text()'))[0]
            taskData = (singlePageTree.xpath('/html/body/div[2]/main/section/div/div/div/div[1]/div[2]/text()'))[0].split(',')[0]
            taskDescription = singlePageTree.xpath('/html/body/div[2]/main/section/div/div/div/div[1]/div[4]/descendant::text()')
            fullDesc = ""
            for description in taskDescription:
                fullDesc = fullDesc + description + " "
            print(taskTitle, taskData, fullDesc)
            file.write(link)
            file.write(taskTitle)
            file.write(taskData)
            file.write(fullDesc)
            file.write("\n")
        else:
            break
    file.close()



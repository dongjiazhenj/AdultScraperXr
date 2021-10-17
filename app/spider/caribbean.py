# -*- coding: utf-8 -*-

from app.spider.uncensored_spider import UnsensoredSpider


class Caribbean(UnsensoredSpider):

    basicUrl = 'www.caribbeancom.com'

    def search(self, q):

        '''
        执行查询函数
        '''
        item = []
        '获取查询结果页html对象'
        url = 'https://%s/moviepages/%s/index.html' % (self.basicUrl, q)
        html_item = self.getHtmlByurl(url)
        if html_item['issuccess']:
            media_item = self.analysisMediaHtmlByxpath(
                html_item['html'], q)
            item.append({'issuccess': True, 'data': media_item})
        else:
            pass  # print repr(html_item['ex'])

        return item

    def analysisMediaHtmlByxpath(self, html, q):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """
        media = self.media.copy()
        number = self.tools.cleanstr(q.upper())
        media.update({'m_number': number})

        xpath_title = "//div[@class='video-detail']/h1/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            media.update({'m_title': title})

        xpath_summary = "//div[@class='movie-comment']/p/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.update({'m_summary': summary})

        media.update({'m_poster': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})
        media.update({'m_art_url': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})

        studio = 'Caribbeancom'
        media.update({'m_studio': studio})

        directors = ''
        media.update({'m_directors': directors})

        collections = 'Caribbeancom'
        media.update({'m_collections': collections})

        xpath_year = "//div[@class='movie-info']/dl[3]/dd"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0].text)
            media.update({'m_year': year})
            media.update({'m_originallyAvailableAt': year})

        xpath_category = "//dl[@class='movie-info-cat']/dd/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        actor = {}
        xpath_actor_name = "//div[@class='movie-info']/dl[1]/dd/a/span/text()"
        actor_name = html.xpath(xpath_actor_name)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):

                actor.update({self.tools.cleanstr2(
                    actorname): ''})

            media.update({'m_actor': actor})

        return media

from django.utils.safestring import mark_safe

class Paginator(object):

    def __init__(self,current_page,total_item_count,base_url,per_page_count=10,show_pager_count=11):
        """
        :param current_page:  当前页码
        :param total_item_count: 数据库数据总条数
        :param base_url: 分页前缀URL
        :param per_page_count:   每页显示数据条数
        :param show_pager_count: 对多显示的页码
        """
        self.current_page = current_page
        self.total_item_count = total_item_count
        self.base_url = base_url
        self.per_page_count = per_page_count
        self.show_pager_count = show_pager_count

        #获取页码数及最后一页上显示的条目数
        max_pager_num, b = divmod(total_item_count, per_page_count)

        if b:
            max_pager_num += 1
        self.max_pager_num = max_pager_num

    @property
    def start(self):
        """
        #每一页显示的第一条数据
        :return:
        """
        return (self.current_page-1)* self.per_page_count

    @property
    def end(self):
        """
        #每一页显示的最后一条数据
        :return:
        """
        return self.current_page * self.per_page_count

    def page_html(self):
        """

        :return:
        """
        page_list = []

        #如果当前页为第1页,则上一页按钮不可用
        if self.current_page == 1:
            prev = ' <li><a href="#">上一页</a></li>'
        else:
            prev = ' <li><a href="%s?page=%s">上一页</a></li>' % (self.base_url,self.current_page - 1,)
        page_list.append(prev)

        half_show_pager_count = int(self.show_pager_count / 2)

        # 页面显示的总页数小于定义的页面上显示的页数时
        if self.max_pager_num < self.show_pager_count:
            pager_start = 1
            pager_end = self.max_pager_num + 1
        else:
            #当前页码数小于定义的页面显示的页数的一半时
            if self.current_page <= half_show_pager_count:
                pager_start = 1
                pager_end = self.show_pager_count + 1
            else:
                #当前面码数大于定义的页面显示的页数的一半时
                if self.current_page + half_show_pager_count > self.max_pager_num:
                    pager_start = self.max_pager_num - self.show_pager_count + 1
                    pager_end = self.max_pager_num + 1
                else:
                    #正常显示的时候
                    pager_start = self.current_page - half_show_pager_count
                    pager_end = self.current_page + half_show_pager_count + 1

        #遍历循环当前页的每一条记录
        for i in range(pager_start, pager_end):
            if i == self.current_page:
                tpl = ' <li class="active"><a href="%s?page=%s">%s</a></li>' % (self.base_url,i, i,)
            else:
                tpl = ' <li><a href="%s?page=%s">%s</a></li>' % (self.base_url,i, i,)
            page_list.append(tpl)

        # 如果当前页为最后一页,则下一页按钮不可用
        if self.current_page == self.max_pager_num:
            next = ' <li><a href="#">下一页</a></li>'
        else:
            next = ' <li><a href="%s?page=%s">下一页</a></li>' % (self.base_url,self.current_page + 1,)
        page_list.append(next)

        return mark_safe(''.join(page_list))
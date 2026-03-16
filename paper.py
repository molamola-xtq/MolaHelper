import arxiv
import datetime



def arxiv_search(query: str,max_results: int = 5):
    # 执行搜索并获取结果
    print(query)
    client = arxiv.Client()
# 构建搜索条件
    search = arxiv.Search(
    query=query,
    max_results=max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate
)
    string = ""
    try:
        results = client.results(search)
        for result in results:
            string += f"title: {result.title}\n"
            string += f"url: {result.pdf_url}\n"
            string += f"updated: {result.updated}\n"
            string += f"summary: {result.summary}\n"
            string += "\n"
    except:
        string = "查询失败,网络连接失败"
        return ['ERROR',string]
    return ['OK',string]
    


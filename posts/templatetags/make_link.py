from django import template
register = template.Library()

# 해시태그를 하나하나 a태그로 감싸는 것을 할것

@register.filter
def hashtag_link(post):
    content = post.content # #고양이 야옹 #강아지 멍멍
    hashtags = post.hashtags.all() # QuerySet[HashTag object(1:고양이), HashTag object(2:강아지)]

    for hashtag in hashtags:
        # replace(과거데이터, 바꿀데이터)
        content = content.replace(f'{hashtag.content}', f'<a href="/posts/hashtags/{hashtag.id}">{hashtag.content}</a>')
    return content
 from django.contrib.auth.models import User
 from news_portal.models import Author, Category, Post, PostCategory, Comment
 from news_portal import ITEM, article

#Создать двух пользователей (с помощью метода User.objects.create_user('username')).
 u1 = User.objects.create_user(username='Vasja')
 u2 = User.objects.create_user(username='Fedja')

#Создать два объекта модели Author, связанные с пользователями.
 a1 = Author.objects.create(user = u1)
 a2 = Author.objects.create(user = u2)

#Добавить 4 категории в модель Category.
 cat1 = Category.objects.create(category = 'cat1')
 cat2 = Category.objects.create(category = 'cat2')
 cat3 = Category.objects.create(category = 'cat3')
 cat4 = Category.objects.create(category = 'cat4')

#Добавить 2 статьи и 1 новость.
 p1 = Post.objects.create(author=a1, heading='head1', text='text1')
 p2 = Post.objects.create(author=a1,item='NEW', heading='head2', text='text2')
 p3 = Post.objects.create(author=a2,item='NEW', heading='head3', text='text3')

#Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
 pc1 = PostCategory.objects.create(post=p1, category=cat1)
 pc2 = PostCategory.objects.create(post=p2, category=cat2)
 pc3 = PostCategory.objects.create(post=p2, category=cat3)
 pc4 = PostCategory.objects.create(post=p3, category=cat4)

#Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
 com1 = Comment.objects.create(post=p1, user=a1.user, comment_text='comment1')
 com2 = Comment.objects.create(post=p2, user=a1.user, comment_text='comment2')
 com3 = Comment.objects.create(post=p3, user=a2.user, comment_text='comment3')
 com4 = Comment.objects.create(post=p1, user=a2.user, comment_text='comment4')

#Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
 p1.like()
 p1.like()
 p1.dislike()
 p1.like()
 p1.like()
 p2.like()
 p3.like()
 p3.dislike()
 p3.dislike()
 p3.dislike()
 com1.like()
 com2.dislike()
 com3.like()
 com4.dislike()

#Обновить рейтинги пользователей.
 a1.update_rating()
 a2.update_rating()

#Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
 print(Author.objects.order_by('-user_rating').values('user__username','user_rating').first())

#Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
 pr=Post.objects.order_by('-rating').first()
 print('дата добавления - ',pr.date,'|username - ', pr.author.user,'|рейтинг - ', pr.rating,'|заголовок - ', pr.heading,'|превью лучшей статьи - ', pr.preview())

#Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
 list1 = list(Comment.objects.filter(post=pr.id))
 for i in list1: print('дата создания - ',i.date,'|рейтинг - ',i.rating,'|текст комментария - ',i.comment_text,'|username - ',i.user)

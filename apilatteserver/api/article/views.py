import gzip, json
from slugify import slugify
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer, AllArticleSerializer
from django.middleware.gzip import GZipMiddleware
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import Http404

gzip_middleware = GZipMiddleware()

def data_to_gzip(data):
    file_name = 'gz-warehouse/article.gz'
    with gzip.GzipFile(file_name, 'w') as fout:
        fout.write(json.dumps(data).encode('utf-8'))
    return file_name


class GetAllArticles(generics.ListAPIView):
    
    def get(self, request):
        articles = Article.objects.filter(is_archived=False).order_by('-id')
        serializer = AllArticleSerializer(articles, many=True)
        res_data = list(serializer.data)
        gzip_file_name = data_to_gzip(res_data)
        response = HttpResponse(open(gzip_file_name, 'rb'))
        response['Content-Encoding'] = 'gzip'
        return response


class CreateArticle(generics.CreateAPIView):

    def post(self, request):
        try:
            req_data = request.data.copy()
            serializer = ArticleSerializer(data=req_data)
            if serializer.is_valid():
                new_article = Article(**serializer.validated_data)
                new_article.save()
                new_article.slug = slugify('-'.join([new_article.title, str(new_article.id)]))
                new_article.img_url = req_data['imgUrl']
                new_article.save()
                res = HttpResponse(str({
                    'detail': 'success',
                    'id': new_article.id,
                    'slug': new_article.slug
                }), content_type='application/json', status=201)
            return res
        except Exception as e:
            print(str(e))


class ArticleById(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, id):
        article = get_object_or_404(Article, id=id, is_archived=False)
        res_data = model_to_dict(article)
        gzip_file_name = data_to_gzip(res_data)
        response = HttpResponse(open(gzip_file_name, 'rb'))
        response['Content-Encoding'] = 'gzip'
        return response
        
    def put(self, request, id):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Article.objects.filter(id=id, is_archived=False).update(**serializer.validated_data)
                article = Article.objects.get(id=id)
                article.slug = slugify('-'.join([article.title, str(article.id)]))
                article.save()
            except Article.DoesNotExist:
                raise Http404({'detail': 'article does not exist'})
            return HttpResponse({'detail': 'update success'}, status=204)
        return HttpResponse({'detail': 'fail'}, status=401)

    def delete(self, request, id):
        article = get_object_or_404(Article, id=id, is_archived=False)
        article.is_archived = True
        article.save()
        return HttpResponse({'detail': 'delete success'}, status=204)

    def patch(self, request, id):
        return HttpResponse({'detail': 'PATCH: not support'}, status=400)


class ArticleBySlug(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, is_archived=False)
        res_data = model_to_dict(article)
        gzip_file_name = data_to_gzip(res_data)
        response = HttpResponse(open(gzip_file_name, 'rb'))
        response['Content-Encoding'] = 'gzip'
        return response

    def put(self, request, slug):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Article.objects.filter(slug=slug, is_archived=False).update(**serializer.validated_data)
            except Article.DoesNotExist:
                raise Http404({'detail': 'article does not exist'})
            return HttpResponse({'detail': 'update success'}, status=204)
        return HttpResponse({'detail': 'fail'}, status=401)

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug, is_archived=False)
        article.is_archived = True
        article.save()
        return HttpResponse({'detail': 'delete success'}, status=204)

    def patch(self, request, slug):
        return HttpResponse({'detail': 'PATCH: not support'}, status=400)


class SetArticleOnCarousel(generics.ListCreateAPIView):

    def get(self, request, id):
        article = get_object_or_404(Article, id=id, is_archived=False)
        article.show_on_carousel = True
        article.save()
        # return JsonResponse({"detail": "set on carousel success"}, status=200)
        return HttpResponse(content='{"detail": "set on carousel success"}'.encode(), status=200)
        # return HttpResponse({'detail': 'GET: not support'}, status=400)

    def post(self, request, id):
        # article = get_object_or_404(Article, id=id, is_archived=False)
        # article.show_on_carousel = True
        # article.save()
        # return HttpResponse({'detail': 'set on carousel success'}, status=204)
        return HttpResponse({'detail': 'POST: not support'}, status=400)
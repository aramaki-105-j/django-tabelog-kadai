from django.shortcuts import redirect, render
from tabelog.models import Like
from django.views.generic import CreateView, DeleteView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy



class LikeCreateView(UserPassesTestMixin, CreateView):

    model = Like
        
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')
    

    def post(self, request, *args, **kwargs):
        Like.objects.create(
            store_id = kwargs['store_id'],
            user_id = request.user.id,
        )
        
        return redirect('store_detail', kwargs['store_id'])


class LikeCancelView(UserPassesTestMixin, CreateView):
    model = Like
        
    def test_func(self):
        like = Like.objects.get(store_id=self.kwargs['pk'], user_id=self.request.user.id)
        return self.request.user.is_authenticated and self.request.user.is_paid and like.user_id == self.request.user.id

    def handle_no_permission(self):
        return redirect('home')

    def post(self, request,**kwargs):
        Like.objects.filter(user_id=request.user.id, store_id=kwargs['pk']).delete()
        return redirect('store_detail', kwargs['pk'])

class LikeListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('home')

    def get(self, request, *args, **kwargs):
        like_data = Like.objects.filter(user_id=request.user.id)

        return render(request, 'store/like_list.html', {
            'like_data': like_data,
        })
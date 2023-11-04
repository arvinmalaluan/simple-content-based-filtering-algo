from django.urls import path
from .views import PostList, PostDetail, Comment, EngagementSetter, ResumePost, ProfilePost, ResumePut, ProfilePut, EngagementPut, CommentPut, GetAll, PWRoles, GAUWP, get_unique_users_last_three_days, get_post_with_profiles

from chat.views import create_new_message, Conversation, Messages, ConversationUpdate

urlpatterns = [
    path('create-post', PostList.as_view()),
    path('create-post/<int:pk>', PostDetail.as_view()),
    path('create-comment', Comment.as_view()),
    path('create-engagement', EngagementSetter.as_view()),

    path('create-resume', ResumePost.as_view()),
    path('create-profile', ProfilePost.as_view()),

    path('create-resume/<int:account>', ResumePut.as_view()),
    path('create-profile/<int:account>', ProfilePut.as_view()),
    path('create-engagement/<int:custom_key>', EngagementPut.as_view()),
    path('create-comment/<int:pk>', CommentPut.as_view()),

    path('admin-getusers', GAUWP.as_view()),

    # path('get-all', views.get_all_posts, name='get-all'),
    path('', create_new_message),
    path('get', get_unique_users_last_three_days),
    path('get-w-roles', PWRoles.as_view()),
    path('get-messages/', Messages.as_view()),
    path('get-messages/hey', Conversation.as_view()),
    path('get-messages/hey/<int:custom_key>', ConversationUpdate.as_view()),
    path('hey', GetAll.as_view()),

    path('test', get_post_with_profiles)

]

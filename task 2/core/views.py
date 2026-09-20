from django.shortcuts import render

def home_view(request):
    """
    Renders the home feed with 2-3 sample posts demonstrating user profile,
    image, caption, like button/count, comments, and comment interactions.
    """
    sample_posts = [
        {
            "id": 1,
            "author_name": "Nathan Rusl",
            "username": "nathanrsl",
            "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=200&q=80",
            "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
            "caption": "Nature's beauty is the best remedy for a restless soul. Finding peace in delicate petals and morning stillness. 🌸✨ #FindYourPeace",
            "time_ago": "2h ago",
            "likes_count": 12300,
            "formatted_likes": "12.3K",
            "is_liked": False,
            "comments_count": 100,
            "comments": [
                {
                    "id": 101,
                    "username": "clara_m",
                    "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100&q=80",
                    "text": "This flower detail is mesmerizing! What lens did you use?",
                    "time": "1h ago"
                },
                {
                    "id": 102,
                    "username": "elena_w",
                    "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=100&q=80",
                    "text": "Absolute serenity in a single frame. The lighting is pure art.",
                    "time": "45m ago"
                },
                {
                    "id": 103,
                    "username": "david_k",
                    "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
                    "text": "So crisp and calming! Beautiful capture brother. 🌿",
                    "time": "20m ago"
                }
            ]
        },
        {
            "id": 2,
            "author_name": "Samantha Raol",
            "username": "raolsmnt",
            "avatar": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=200&q=80",
            "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80",
            "caption": "Golden hour glow and autumn wool layers. Embracing slower mornings and quiet reflections. 🍂☕",
            "time_ago": "5h ago",
            "likes_count": 8450,
            "formatted_likes": "8.4K",
            "is_liked": True,
            "comments_count": 76,
            "comments": [
                {
                    "id": 201,
                    "username": "marcus_art",
                    "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=100&q=80",
                    "text": "The tones in this portrait are so warm and cinematic!",
                    "time": "4h ago"
                },
                {
                    "id": 202,
                    "username": "sofia_lens",
                    "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=100&q=80",
                    "text": "Such a cozy aesthetic, totally in love with this palette ✨",
                    "time": "2h ago"
                }
            ]
        },
        {
            "id": 3,
            "author_name": "Rachel Flowear",
            "username": "rachelflow",
            "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80",
            "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1200&q=80",
            "caption": "Mid-century corners and warm ambient lighting. A peaceful Sunday afternoon sanctuary. 🕯️🛋️",
            "time_ago": "1d ago",
            "likes_count": 2280,
            "formatted_likes": "2.2K",
            "is_liked": False,
            "comments_count": 42,
            "comments": [
                {
                    "id": 301,
                    "username": "interior_hub",
                    "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=100&q=80",
                    "text": "Where is that floor lamp from? The ambient glow is immaculate!",
                    "time": "18h ago"
                },
                {
                    "id": 302,
                    "username": "rachelflow",
                    "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=100&q=80",
                    "text": "It is a vintage brass find from a local antique market! 😊",
                    "time": "12h ago"
                }
            ]
        }
    ]
    return render(request, 'home.html', {'posts': sample_posts, 'active_page': 'home'})


def profile_view(request):
    """
    Renders user profile with profile picture, username, bio, posts/followers/following counts,
    follow button, and user's post grid.
    """
    profile_data = {
        "full_name": "Rachel Flowear",
        "username": "rachelflow",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80",
        "cover_image": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=1400&q=80",
        "bio": "Visual artist & architectural photographer based in Kyoto 🌸 Capturing quiet spaces, floral geometry, and morning light.",
        "posts_count": 240,
        "followers_count": 47300,
        "formatted_followers": "47.3K",
        "following_count": 32000,
        "formatted_following": "32K",
        "is_following": False,
        "posts": [
            {
                "id": 101,
                "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=600&q=80",
                "caption": "Cozy living room sanctuary with afternoon sun.",
                "likes": "2.2K",
                "comments": "42"
            },
            {
                "id": 102,
                "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80",
                "caption": "Luminescent petal textures under soft studio strobe.",
                "likes": "2.28K",
                "comments": "58"
            },
            {
                "id": 103,
                "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80",
                "caption": "Portrait study in natural daylight.",
                "likes": "4.1K",
                "comments": "89"
            },
            {
                "id": 104,
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
                "caption": "Minimalist Scandinavian interior aesthetic.",
                "likes": "1.9K",
                "comments": "31"
            },
            {
                "id": 105,
                "image": "https://images.unsplash.com/photo-1509281373149-e957c6296406?auto=format&fit=crop&w=600&q=80",
                "caption": "Warm golden hues spilling across wooden floors.",
                "likes": "3.5K",
                "comments": "64"
            },
            {
                "id": 106,
                "image": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=600&q=80",
                "caption": "Spring blossom overhead in the courtyard.",
                "likes": "5.7K",
                "comments": "112"
            },
        ]
    }
    return render(request, 'profile.html', {'profile': profile_data, 'active_page': 'profile'})

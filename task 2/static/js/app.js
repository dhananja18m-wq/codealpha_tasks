/**
 * Aura Social — Application JavaScript (Vanilla JS only)
 * Handles client-side UI interactions for Phase 1:
 * - Like/Unlike toggles & micro-animations
 * - Follow/Following toggle & count updates
 * - Comment additions (inline & modal drawer)
 * - Double-tap image like effect
 * - Smooth page transitions & progress bar
 * - Scroll-based reveal animations
 * - Skeleton loading simulator
 */

document.addEventListener('DOMContentLoaded', () => {
    initPageTransitions();
    initLikeInteractions();
    initDoubleTapToLike();
    initCommentInteractions();
    initCommentModal();
    initFollowInteraction();
    initScrollReveal();
    initSkeletonSimulator();
});

/* ==========================================================================
   1. Page Transitions & Progress Bar
   ========================================================================== */
function initPageTransitions() {
    const transitionBar = document.getElementById('pageTransitionBar');
    
    // Complete any active transition bar on load
    if (transitionBar) {
        transitionBar.classList.add('done');
        setTimeout(() => {
            transitionBar.classList.remove('loading', 'done');
        }, 400);
    }

    // Intercept internal navigation for smooth feel
    const internalLinks = document.querySelectorAll('a[href^="/"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            // Ignore hash links or same-page anchor
            if (!href || href === '#' || href === window.location.pathname) return;

            // Start progress bar animation
            if (transitionBar) {
                transitionBar.classList.add('loading');
            }
        });
    });
}

/* ==========================================================================
   2. Like / Unlike Post Interactions
   ========================================================================== */
function initLikeInteractions() {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            togglePostLike(button);
        });
    });
}

function togglePostLike(button, forceState = null) {
    const isCurrentlyLiked = button.getAttribute('data-liked') === 'true';
    const targetState = forceState !== null ? forceState : !isCurrentlyLiked;
    const postId = button.getAttribute('data-post-id');
    const countElement = button.querySelector('.likes-count');
    const heartSvg = button.querySelector('.heart-icon svg');
    let currentRawCount = parseInt(button.getAttribute('data-likes-count') || '0', 10);

    if (targetState) {
        // Liked
        button.classList.add('liked', 'pop-heart');
        button.setAttribute('data-liked', 'true');
        button.setAttribute('aria-pressed', 'true');
        button.setAttribute('aria-label', 'Unlike post');
        if (heartSvg) {
            heartSvg.setAttribute('fill', '#fa5a3e');
        }
        currentRawCount += 1;
    } else {
        // Unliked
        button.classList.remove('liked');
        button.classList.add('pop-heart');
        button.setAttribute('data-liked', 'false');
        button.setAttribute('aria-pressed', 'false');
        button.setAttribute('aria-label', 'Like post');
        if (heartSvg) {
            heartSvg.setAttribute('fill', 'none');
        }
        currentRawCount = Math.max(0, currentRawCount - 1);
    }

    // Remove animation class after playback
    setTimeout(() => {
        button.classList.remove('pop-heart');
    }, 450);

    // Update count display
    button.setAttribute('data-likes-count', currentRawCount);
    if (countElement) {
        countElement.textContent = formatCount(currentRawCount);
    }
}

function formatCount(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    }
    return num.toLocaleString();
}

/* ==========================================================================
   3. Double Tap / Double Click on Post Media to Like
   ========================================================================== */
function initDoubleTapToLike() {
    const mediaContainers = document.querySelectorAll('.post-media-container');

    mediaContainers.forEach(container => {
        let lastTap = 0;
        const postId = container.getAttribute('data-post-id');
        const heartOverlay = container.querySelector('.floating-heart');
        const correspondingLikeBtn = document.querySelector(`.like-btn[data-post-id="${postId}"]`);

        const triggerDoubleTapHeart = () => {
            if (heartOverlay) {
                heartOverlay.classList.remove('animate-heart');
                void heartOverlay.offsetWidth; // Force CSS reflow
                heartOverlay.classList.add('animate-heart');
                setTimeout(() => {
                    heartOverlay.classList.remove('animate-heart');
                }, 800);
            }

            // Ensure post is liked
            if (correspondingLikeBtn && correspondingLikeBtn.getAttribute('data-liked') !== 'true') {
                togglePostLike(correspondingLikeBtn, true);
            }
        };

        // Desktop double click
        container.addEventListener('dblclick', (e) => {
            e.preventDefault();
            triggerDoubleTapHeart();
        });

        // Mobile touch double-tap
        container.addEventListener('touchend', (e) => {
            const currentTime = new Date().getTime();
            const tapGap = currentTime - lastTap;
            if (tapGap < 300 && tapGap > 0) {
                e.preventDefault();
                triggerDoubleTapHeart();
            }
            lastTap = currentTime;
        });
    });
}

/* ==========================================================================
   4. Follow / Following Profile Toggle
   ========================================================================== */
function initFollowInteraction() {
    const followBtn = document.getElementById('profileFollowBtn');
    const followersCountElem = document.getElementById('followersCount');
    const followBtnText = document.getElementById('followBtnText');

    if (!followBtn) return;

    followBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const isCurrentlyFollowing = followBtn.getAttribute('data-following') === 'true';
        const willFollow = !isCurrentlyFollowing;
        let baseCount = parseInt(followersCountElem ? followersCountElem.getAttribute('data-base-count') || '47300' : '47300', 10);

        if (willFollow) {
            followBtn.classList.add('following', 'just-followed');
            followBtn.setAttribute('data-following', 'true');
            followBtn.setAttribute('aria-pressed', 'true');
            if (followBtnText) followBtnText.textContent = 'Following';
            baseCount += 1;
        } else {
            followBtn.classList.remove('following', 'just-followed');
            followBtn.setAttribute('data-following', 'false');
            followBtn.setAttribute('aria-pressed', 'false');
            if (followBtnText) followBtnText.textContent = 'Follow';
            baseCount = Math.max(0, baseCount - 1);
        }

        setTimeout(() => {
            followBtn.classList.remove('just-followed');
        }, 400);

        if (followersCountElem) {
            followersCountElem.setAttribute('data-base-count', baseCount);
            followersCountElem.textContent = formatCount(baseCount);
        }
    });
}

/* ==========================================================================
   5. Inline Comment Submission
   ========================================================================== */
function initCommentInteractions() {
    const commentForms = document.querySelectorAll('.inline-comment-form');

    commentForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = form.querySelector('.inline-comment-input');
            const postId = form.getAttribute('data-post-id');
            const text = input ? input.value.trim() : '';

            if (!text) return;

            addNewCommentToPost(postId, 'rachelflow', text, 'Just now');

            // Reset input and keep focus friendly
            if (input) {
                input.value = '';
                input.blur();
            }
        });
    });
}

function addNewCommentToPost(postId, username, text, timeText) {
    const postCommentsList = document.getElementById(`post-comments-list-${postId}`);
    const postCard = document.getElementById(`post-${postId}`);

    if (postCommentsList) {
        const commentDiv = document.createElement('div');
        commentDiv.className = 'comment-item comment-new';
        commentDiv.innerHTML = `
            <div class="comment-content">
                <span class="comment-username">${escapeHtml(username)}</span>
                <span class="comment-text">${escapeHtml(text)}</span>
            </div>
            <span class="comment-time">${escapeHtml(timeText)}</span>
        `;
        postCommentsList.appendChild(commentDiv);
    }

    // Increment post comment counter
    if (postCard) {
        const commentCountBadge = postCard.querySelector('.comments-count');
        if (commentCountBadge) {
            const currentCount = parseInt(commentCountBadge.textContent || '0', 10);
            commentCountBadge.textContent = (currentCount + 1).toString();
        }
    }
}

/* ==========================================================================
   6. Expanded Comments Drawer / Modal
   ========================================================================== */
let activeModalPostId = null;

function initCommentModal() {
    const commentModal = document.getElementById('commentModal');
    const closeModalBtn = document.getElementById('closeCommentModalBtn');
    const modalForm = document.getElementById('modalCommentForm');
    const modalInput = document.getElementById('modalCommentInput');
    const modalCommentsList = document.getElementById('modalCommentsList');

    if (!commentModal) return;

    // Trigger modal from card comment buttons and "view all comments" links
    document.querySelectorAll('.comment-btn, .btn-view-all-comments').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const postId = trigger.getAttribute('data-post-id');
            openCommentModal(postId);
        });
    });

    const closeModal = () => {
        commentModal.classList.remove('open');
        commentModal.setAttribute('aria-hidden', 'true');
        activeModalPostId = null;
    };

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    // Close on backdrop click
    commentModal.addEventListener('click', (e) => {
        if (e.target === commentModal) {
            closeModal();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && commentModal.classList.contains('open')) {
            closeModal();
        }
    });

    // Handle comment submit inside modal
    if (modalForm && modalInput) {
        modalForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = modalInput.value.trim();
            if (!text || !activeModalPostId) return;

            // Append to modal comments view
            const newCard = document.createElement('div');
            newCard.className = 'modal-comment-card comment-new';
            newCard.innerHTML = `
                <img src="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=100&q=80" alt="Rachel" class="modal-comment-avatar">
                <div class="modal-comment-body">
                    <p><strong class="modal-comment-author">rachelflow</strong> <span class="modal-comment-text">${escapeHtml(text)}</span></p>
                    <div class="modal-comment-meta">Just now</div>
                </div>
            `;
            modalCommentsList.appendChild(newCard);
            newCard.scrollIntoView({ behavior: 'smooth' });

            // Also mirror comment onto the card on the feed
            addNewCommentToPost(activeModalPostId, 'rachelflow', text, 'Just now');

            modalInput.value = '';
        });
    }
}

function openCommentModal(postId) {
    const commentModal = document.getElementById('commentModal');
    const modalCommentsList = document.getElementById('modalCommentsList');
    const postCard = document.getElementById(`post-${postId}`);

    if (!commentModal || !modalCommentsList || !postCard) return;

    activeModalPostId = postId;
    modalCommentsList.innerHTML = '';

    // Extract comments from the post card to populate the modal
    const commentItems = postCard.querySelectorAll('.inline-comments-list .comment-item');
    
    if (commentItems.length === 0) {
        modalCommentsList.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 24px 0;">No comments yet. Be the first to comment!</div>';
    } else {
        commentItems.forEach(item => {
            const user = item.querySelector('.comment-username')?.textContent || 'User';
            const text = item.querySelector('.comment-text')?.textContent || '';
            const time = item.querySelector('.comment-time')?.textContent || '';

            const card = document.createElement('div');
            card.className = 'modal-comment-card';
            card.innerHTML = `
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80" alt="${escapeHtml(user)}" class="modal-comment-avatar">
                <div class="modal-comment-body">
                    <p><strong class="modal-comment-author">${escapeHtml(user)}</strong> <span class="modal-comment-text">${escapeHtml(text)}</span></p>
                    <div class="modal-comment-meta">${escapeHtml(time)}</div>
                </div>
            `;
            modalCommentsList.appendChild(card);
        });
    }

    commentModal.classList.add('open');
    commentModal.setAttribute('aria-hidden', 'false');
    
    // Focus input after transition
    setTimeout(() => {
        const input = document.getElementById('modalCommentInput');
        if (input) input.focus();
    }, 200);
}

/* ==========================================================================
   7. Scroll-based Reveal Animations
   ========================================================================== */
function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;

    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-revealed');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   8. Skeleton Loading Simulator
   ========================================================================== */
function initSkeletonSimulator() {
    const toggleBtn = document.getElementById('simulateLoadingBtn');
    const skeletonContainer = document.getElementById('feedSkeletonContainer');
    const postsStream = document.getElementById('postsFeedStream');

    if (!toggleBtn || !skeletonContainer || !postsStream) return;

    toggleBtn.addEventListener('click', () => {
        postsStream.style.display = 'none';
        skeletonContainer.style.display = 'block';
        toggleBtn.disabled = true;

        setTimeout(() => {
            skeletonContainer.style.display = 'none';
            postsStream.style.display = 'flex';
            
            // Re-trigger staggered animation
            const cards = postsStream.querySelectorAll('.post-card');
            cards.forEach(card => {
                card.style.animation = 'none';
                void card.offsetWidth; // Reflow
                card.style.animation = '';
            });

            toggleBtn.disabled = false;
        }, 650);
    });
}

/* ==========================================================================
   Helper: Basic HTML Escaping
   ========================================================================== */
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

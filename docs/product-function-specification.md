# Product Function Specification
## Birthday Social Network Platform

**Version:** 1.0
**Last Updated:** 2025-11-17
**Status:** Draft

---

## 1. Project Overview

### 1.1 Purpose
A social networking platform that connects people who share the same birthday, fostering unique communities based on birth dates. Users can discover others born on the same day, communicate through messaging and posts, and join birthday-based communities.

### 1.2 Target Audience
- Individuals interested in connecting with birthday twins
- People looking for unique social connections
- Users who enjoy community-based social interactions

### 1.3 Tech Stack
- **Frontend:** HTML5, CSS3 (Tailwind CSS), JavaScript (Vue.js)
- **Backend:** Python (FastAPI)
- **Database:** SQLite (development), PostgreSQL (recommended for production)
- **Authentication:** Email/Password + OAuth (Google/Facebook)

---

## 2. Core Features

### 2.1 User Registration & Authentication

#### 2.1.1 Registration Requirements
**Required Information:**
- Email address
- Password (min 8 characters, must include uppercase, lowercase, number)
- Full name
- Date of birth (MM/DD/YYYY)
- Gender (Male/Female/Other/Prefer not to say)
- City/Region (for location-based matching)

**Optional Information:**
- Profile picture
- Bio/About me (max 500 characters)
- Interests/Hobbies

#### 2.1.2 Authentication Methods
1. **Email + Password**
   - Email verification required upon registration
   - Password reset via email
   - Session management with JWT tokens

2. **Social Login (OAuth)**
   - Google OAuth 2.0
   - Facebook Login
   - Auto-populate profile data from social accounts

#### 2.1.3 Security Requirements
- Password hashing (bcrypt)
- HTTPS only
- CSRF protection
- Rate limiting on login attempts
- Session timeout after 30 days of inactivity

---

### 2.2 User Profile Management

#### 2.2.1 Profile Information
**Public Information:**
- Display name
- Birthday (month/day only, year optional)
- City/Region
- Gender (if user chooses to display)
- Profile picture
- Bio
- Member since date

**Private Information:**
- Email address
- Full date of birth (year)
- Exact address (not collected)
- Password

#### 2.2.2 Profile Actions
- Edit profile information
- Upload/change profile picture
- Update privacy settings
- Delete account

---

### 2.3 Birthday Matching & Search

#### 2.3.1 Automatic Matching
- System automatically finds users with the same birthday (month/day)
- Display birthday matches on user dashboard
- Show number of birthday twins on platform

#### 2.3.2 Search & Filter Functionality
**Search Criteria:**
- Birthday (specific date or month)
- City/Region
- Gender
- Age range (calculated from birth year if public)

**Search Results Display:**
- Profile picture
- Display name
- Birthday
- City/Region
- Short bio preview
- "Connect" or "Message" button

#### 2.3.3 Privacy Controls
- Users can opt-out of being discoverable in search
- Users can hide specific profile fields
- Block/report functionality

---

### 2.4 Messaging System

#### 2.4.1 Direct Messaging
**Type:** Asynchronous messaging (no real-time WebSocket required)

**Features:**
- One-on-one conversations
- Message history
- Unread message indicators
- Message timestamps
- Text messages only (Phase 1)
- Future: Image/file sharing (Phase 2)

**User Flow:**
1. User clicks "Message" on another user's profile
2. Opens conversation thread
3. Type and send messages
4. Recipient sees notification on next page load/refresh
5. Messages appear in chronological order

#### 2.4.2 Message Notifications
- In-app notification badge (unread count)
- Email notification for new messages (optional, user setting)
- Notification list showing recent message previews

---

### 2.5 Social Feed & Posts

#### 2.5.1 Post Creation
**Post Types:**
- Text posts (max 2000 characters)
- Optional: Image posts (future phase)

**Post Visibility Options:**
- Public (visible to all users)
- Birthday twins only (same birthday)
- Specific group only

**Post Features:**
- Title/Caption
- Post content
- Timestamp
- Author information
- Like counter
- Comment counter

#### 2.5.2 Commenting System
**Features:**
- Users can comment on any visible post
- Comments display author name, profile picture, timestamp
- Nested comments (1 level deep max)
- Like comments
- Edit/delete own comments
- Report inappropriate comments

**Moderation:**
- Post author can delete comments on their posts
- Users can report posts/comments
- Admin moderation panel (future phase)

#### 2.5.3 Feed Algorithm
**Main Feed:**
- Chronological display of posts
- Filter options: All posts, Birthday twins only, Following
- Pagination (20 posts per page)

---

### 2.6 Groups & Communities

#### 2.6.1 Birthday-Based Groups
**Auto-Generated Groups:**
- Each unique birthday has an automatic group (e.g., "January 1st Community")
- Users are automatically members of their birthday group
- Group member count visible

#### 2.6.2 Group Features
**Group Page Includes:**
- Group name and description
- Member list (sortable by join date, activity)
- Group feed (posts visible only to group members)
- Group statistics (member count, post count)

**Group Actions:**
- Post to group feed
- View all group members
- Search within group members (by location, gender)
- Leave group (hide from groups, but can rejoin)

#### 2.6.3 Custom Groups (Future Phase)
- Users can create interest-based groups
- Invite-only or public groups
- Group admin roles

---

## 3. User Roles & Permissions

### 3.1 Regular User
- Create and manage own profile
- Search for users
- Send messages
- Create posts and comments
- Join birthday groups
- Like posts/comments

### 3.2 Administrator (Future Phase)
- All regular user permissions
- View reported content
- Delete inappropriate posts/comments
- Ban users
- View platform analytics

---

## 4. Data Models

### 4.1 User Model
```
User {
  id: UUID
  email: String (unique, required)
  password_hash: String (required)
  full_name: String (required)
  display_name: String
  birth_date: Date (required)
  gender: Enum (required)
  city: String (required)
  region: String (required)
  profile_picture_url: String
  bio: String (max 500 chars)
  is_discoverable: Boolean (default: true)
  email_verified: Boolean (default: false)
  oauth_provider: String (nullable)
  oauth_id: String (nullable)
  created_at: DateTime
  updated_at: DateTime
  last_login: DateTime
}
```

### 4.2 Message Model
```
Message {
  id: UUID
  sender_id: UUID (foreign key to User)
  recipient_id: UUID (foreign key to User)
  content: Text (required)
  is_read: Boolean (default: false)
  created_at: DateTime
  updated_at: DateTime
}
```

### 4.3 Post Model
```
Post {
  id: UUID
  author_id: UUID (foreign key to User)
  title: String (max 200 chars)
  content: Text (max 2000 chars, required)
  visibility: Enum (public, birthday_twins, group)
  group_id: UUID (nullable, foreign key to Group)
  like_count: Integer (default: 0)
  comment_count: Integer (default: 0)
  created_at: DateTime
  updated_at: DateTime
}
```

### 4.4 Comment Model
```
Comment {
  id: UUID
  post_id: UUID (foreign key to Post)
  author_id: UUID (foreign key to User)
  parent_comment_id: UUID (nullable, for nested comments)
  content: Text (max 500 chars, required)
  like_count: Integer (default: 0)
  created_at: DateTime
  updated_at: DateTime
}
```

### 4.5 Group Model
```
Group {
  id: UUID
  name: String (required)
  description: Text
  group_type: Enum (birthday, custom)
  birth_month: Integer (1-12, nullable)
  birth_day: Integer (1-31, nullable)
  member_count: Integer (default: 0)
  created_at: DateTime
  updated_at: DateTime
}
```

### 4.6 GroupMembership Model
```
GroupMembership {
  id: UUID
  user_id: UUID (foreign key to User)
  group_id: UUID (foreign key to Group)
  joined_at: DateTime
  is_active: Boolean (default: true)
}
```

---

## 5. API Endpoints (Summary)

### 5.1 Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/verify-email` - Email verification
- `POST /api/auth/reset-password` - Password reset
- `GET /api/auth/oauth/google` - Google OAuth
- `GET /api/auth/oauth/facebook` - Facebook OAuth

### 5.2 User Profile
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{user_id}` - Get user profile by ID
- `DELETE /api/users/me` - Delete account

### 5.3 Search & Matching
- `GET /api/users/search` - Search users (with filters)
- `GET /api/users/birthday-matches` - Get users with same birthday

### 5.4 Messaging
- `GET /api/messages/conversations` - Get all conversations
- `GET /api/messages/conversation/{user_id}` - Get conversation with specific user
- `POST /api/messages` - Send message
- `PUT /api/messages/{message_id}/read` - Mark message as read

### 5.5 Posts & Feed
- `GET /api/posts/feed` - Get main feed
- `GET /api/posts/{post_id}` - Get specific post
- `POST /api/posts` - Create post
- `PUT /api/posts/{post_id}` - Update post
- `DELETE /api/posts/{post_id}` - Delete post
- `POST /api/posts/{post_id}/like` - Like/unlike post

### 5.6 Comments
- `GET /api/posts/{post_id}/comments` - Get post comments
- `POST /api/posts/{post_id}/comments` - Create comment
- `PUT /api/comments/{comment_id}` - Update comment
- `DELETE /api/comments/{comment_id}` - Delete comment
- `POST /api/comments/{comment_id}/like` - Like/unlike comment

### 5.7 Groups
- `GET /api/groups` - Get all groups
- `GET /api/groups/{group_id}` - Get specific group
- `GET /api/groups/{group_id}/members` - Get group members
- `POST /api/groups/{group_id}/join` - Join group
- `POST /api/groups/{group_id}/leave` - Leave group
- `GET /api/groups/{group_id}/posts` - Get group posts

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Page load time: < 2 seconds
- API response time: < 500ms for 95% of requests
- Support 1000+ concurrent users (Phase 1)

### 6.2 Security
- All data transmission over HTTPS
- SQL injection prevention
- XSS protection
- CSRF tokens for state-changing operations
- Regular security audits

### 6.3 Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatible
- Responsive design (mobile, tablet, desktop)

### 6.4 Browser Support
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

---

## 7. Future Enhancements (Phase 2+)

### 7.1 Advanced Features
- Real-time messaging (WebSocket)
- Video/voice calling
- Image and file sharing in messages
- Advanced search filters (interests, hobbies)
- Friend/connection system
- Birthday reminders and notifications
- Birthday countdown widgets
- Virtual birthday parties/events

### 7.2 Gamification
- User badges and achievements
- Birthday twin leaderboard
- Profile completion percentage
- Activity streaks

### 7.3 Monetization (Future Consideration)
- Premium membership features
- Ad-free experience
- Advanced search filters
- Profile boosting
- Virtual gifts

---

## 8. Success Metrics

### 8.1 User Engagement
- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- Average session duration
- Messages sent per user
- Posts created per user

### 8.2 Growth Metrics
- New user registrations per week
- User retention rate (7-day, 30-day)
- Referral rate

### 8.3 Feature Adoption
- Percentage of users who find birthday matches
- Messaging activity rate
- Post creation rate
- Group participation rate

---

## 9. Development Phases

### Phase 1: MVP (Minimum Viable Product)
**Timeline:** 4-6 weeks
- User registration (email + password only)
- Basic profile management
- Birthday matching
- Simple search (by birthday, city, gender)
- Asynchronous messaging
- Basic post creation and commenting
- Auto-generated birthday groups
- Responsive UI

### Phase 2: Enhanced Features
**Timeline:** 4-6 weeks
- OAuth social login
- Enhanced profile customization
- Image uploads (profile pictures, posts)
- Advanced search filters
- Notification system
- User settings page
- Email notifications

### Phase 3: Community & Growth
**Timeline:** 6-8 weeks
- Custom groups
- Friend/connection system
- Enhanced moderation tools
- Admin dashboard
- Analytics and insights
- Mobile app consideration

---

## 10. Risks & Mitigation

### 10.1 Privacy Concerns
**Risk:** Users may be uncomfortable sharing birthday and location
**Mitigation:**
- Clear privacy policy
- Granular privacy controls
- City/region level only (no exact addresses)
- Opt-out of discovery

### 10.2 Content Moderation
**Risk:** Inappropriate content or harassment
**Mitigation:**
- Report functionality
- Admin moderation tools
- Community guidelines
- Automated content filtering (future)

### 10.3 Scalability
**Risk:** SQLite limitations with growing user base
**Mitigation:**
- Plan migration to PostgreSQL
- Implement caching (Redis)
- Database indexing
- API rate limiting

### 10.4 User Acquisition
**Risk:** Low initial user base makes matching difficult
**Mitigation:**
- Focus on specific demographics initially
- Referral program
- Social media marketing
- Beta testing with engaged community

---

## Appendix A: Glossary

- **Birthday Twin:** Users who share the same birth month and day
- **Asynchronous Messaging:** Message system that doesn't require real-time updates
- **Discovery:** Ability for users to be found in search results
- **OAuth:** Open standard for access delegation (social login)
- **JWT:** JSON Web Token for authentication

---

**Document Status:** Ready for Review
**Next Steps:** Create User Interface Design Document

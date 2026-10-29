---
# Homepage. Every section below is a "block" (layouts/_partials/hbx/blocks/<block>/block.html).
# Reorder, remove or duplicate sections freely; `id` is the anchor used by the menu (config/_default/menus.yaml).
# All content here is placeholder text for a fictional person. Internal links have no leading slash,
# so the site also works under a sub-path (GitHub Pages project sites).
title: ''
summary: ''
date: 2024-01-01
type: landing

design:
  spacing: '2rem'

sections:
  # Hero: portrait, name, role, links, bio and interests, all from data/authors/me.yaml.
  - block: resume-biography-3
    id: bio
    content:
      username: me
    design:
      spacing:
        padding: [0,0,0,0]

  # Research: a lead sentence, an optional feedback-loop figure, the questions that organize your papers
  # (each chip links to a publication page in content/publications/<id>/), and the methods you draw on.
  - block: research-overview
    id: research
    content:
      title: 'Research'
      icon: spark
      lead: 'Three questions run through my work.'
      # The figure: every label is optional (defaults in layouts/_partials/research-plate.html). Delete `plate` to hide it.
      plate:
        left: { title: 'People', caption: ['users · learners', 'decision makers'] }
        right: { title: 'Algorithms', caption: ['models · platforms', 'learning systems'] }
        top: { label: 'Recommendations', caption: 'rankings · rewards · answers' }
        bottom: { label: 'Data & feedback', caption: 'choices · ratings · labels' }
        middle: { label: 'Interaction', caption: 'dynamics · equilibria' }
        # Optional "now" layer for a current focus; delete to hide.
        now:
          text: 'A new question joins the loop'
          left_tag: 'new behaviour'
          right_tag: 'new systems'
          # Phone layout: the pills are narrow, so keep these to about 8 characters.
          left_tag_short: 'behaviour'
          right_tag_short: 'systems'
          left_question: ['Question A:', 'what changes for people?']
          right_question: ['Question B:', 'what changes for systems?']
          compact_questions: ['Question A: what changes for people?', 'Question B: what changes for systems?']
      questions:
        - kicker: 'Theme one'
          title: 'How do recommendation systems change what people choose and create?'
          papers:
            - { id: sample-paper, label: 'Sample paper' }
            - { id: feedback-loops, label: 'Feedback loops' }
        - kicker: 'Theme two'
          title: 'What happens when learning algorithms meet strategic behaviour?'
          papers:
            - { id: strategic-platforms, label: 'Strategic platforms' }
            - { id: game-learning, label: 'Learning in games' }
        - kicker: 'Theme three'
          title: 'How can we measure the welfare that these systems create?'
          papers:
            - { id: early-paper, label: 'An early paper' }
      methods:
        - 'Machine learning'
        - 'Game theory'
        - 'Online learning'
        - 'Causal inference'

  # Publications: newest first from content/publications/. `show` papers are visible; the rest sit behind an expander.
  - block: publication-list
    id: publications
    content:
      title: 'Publications'
      icon: document
      show: 4
      links:
        - { label: 'Full list on Google Scholar', url: 'https://scholar.google.com/' }

  # Teaching: course cards. `url` may be an external course website or a page under content/courses/.
  - block: teaching-overview
    id: teaching
    content:
      title: 'Teaching'
      icon: teach
      lead: 'One or two sentences about what and how you teach. *(Placeholder.)*'
      term: 'Spring 2026 · Example University'
      courses:
        - code: 'DS 101'
          icon: network
          name: 'Introduction to Machine Learning'
          text: 'An undergraduate course: one line on the topics, with weekly labs.'
          url: 'courses/ds-101/'
          cta: 'Course page'
          chips:
            - { icon: academic-cap, label: 'Undergraduate' }
            - { icon: code-bracket, label: 'Python labs' }
        - code: 'DS 520'
          icon: scales
          name: 'Algorithms and Society'
          text: 'A graduate seminar: one line on the topics and the format.'
          url: 'https://example.org/'
          chips:
            - { icon: academic-cap, label: 'Graduate' }
            - { icon: chat-bubble-left-right, label: 'Discussion & case studies' }
      links:
        - { label: 'All courses', url: 'courses/' }

  # News: newest first. `show` items are visible; older ones fold under "Earlier news". Icons: hero/* or custom.
  - block: news-list
    id: news
    content:
      title: 'News'
      icon: news
      show: 5
      items:
        - date: 'Mar 2026'
          icon: microphone
          text: 'Invited talk on feedback loops in recommendation at the Example Workshop, Sample City.'
        - date: 'Jan 2026'
          icon: document-check
          text: 'Our [sample paper](publications/sample-paper/) was accepted at the Example Conference on Machine Learning.'
        - date: 'Dec 2025'
          icon: trophy
          tone: warm
          text: 'Received an example teaching award.'
        - date: 'Sep 2025'
          icon: user-group
          text: 'Co-organized a session on learning systems at the Example Annual Meeting.'
        - date: 'Jul 2025'
          icon: video-camera
          text: 'Online seminar on strategic behaviour in online platforms.'
        - date: 'Jul 2024'
          icon: building-library
          text: 'Joined Example University as an assistant professor.'

  # Beyond research: a short line and chips linking to the cards on the Misc page (content/misc/_index.md).
  - block: misc-teaser
    id: misc
    content:
      title: 'Beyond Research'
      icon: compass
      lead: 'Tennis, cooking, music, two cats, and travel.'
      interests:
        - { icon: tennis, label: 'Tennis', url: 'misc/#tennis' }
        - { icon: cooking, label: 'Cooking', url: 'misc/#kitchen' }
        - { icon: music, label: 'Music', url: 'misc/#music' }
        - { icon: cat, label: 'Cats', url: 'misc/#cats' }
        - { icon: camera, label: 'Travel', url: 'misc/#travel' }
        - { icon: code, label: 'Side projects', url: 'side-projects/' }
      links:
        - { label: 'More about me', url: 'misc/' }
---

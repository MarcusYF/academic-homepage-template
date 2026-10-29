---
# The Misc page: an illustrated bento grid (layouts/_partials/hbx/blocks/profile-bento/block.html).
# Placeholder content. Card fields: id, span (4|5|6|7|8|12), icon, title, art (tennis | kitchen | music | cats | travel,
# drawn in layouts/_partials/misc-art.html), text, facts [{value, label, url}], groups [{label, items}],
# timeline {stages, marks, legend}, link {label, url}, cta (bool). Card ids are anchors (misc/#tennis).
title: 'Beyond Research'
date: 2024-01-01
type: landing

design:
  spacing: '0'

sections:
  - block: profile-bento
    id: misc
    design:
      spacing:
        padding: [0,0,0,0]
    content:
      kicker: Misc
      title: Beyond research
      intro: 'A few things that shape how I think, away from papers.'
      cards:
        - id: path
          span: 12
          icon: path
          title: How I got here
          timeline:
            stages:
              - { label: 'Sample College', years: '2012–16', note: 'BS', from: 2012, to: 2016, kind: study }
              - { label: 'Industry', years: '2016–18', note: 'Example Tech', from: 2016, to: 2018, kind: industry }
              - { label: 'PhD', years: '2018–24', note: 'Another University', from: 2018, to: 2024, kind: study }
              - { label: 'Example University', years: '2024–', note: 'Faculty', from: 2024, to: 2027, kind: now }
            marks:
              - { at: 2021.5, label: 'Research internship, 2021', short: 'Intern' }
            legend:
              - { kind: study, label: 'Study' }
              - { kind: industry, label: 'Industry' }
              - { kind: mark, label: 'Internship' }
          text: 'One or two sentences about your path. *(Placeholder.)*'
          link: { label: 'See my experience', url: 'experience/' }

        - id: tennis
          span: 4
          icon: tennis
          title: Tennis
          art: tennis
          text: 'A short note about a hobby. *(Placeholder.)*'
          facts:
            - { value: '10', label: 'Years playing' }
            - { value: '2×', label: 'Per week' }

        - id: kitchen
          span: 4
          icon: cooking
          title: The kitchen lab
          art: kitchen
          text: 'Cooking as curiosity and experiment more than following recipes.'
          groups:
            - { label: 'Lately', items: ['Example cuisine', 'Another cuisine'] }

        - id: music
          span: 4
          icon: music
          title: Music
          art: music
          text: 'What you listen to or play.'
          groups:
            - { label: 'Favourites', items: ['Artist one', 'Artist two'] }

        - id: cats
          span: 6
          icon: cat
          title: Two cats
          art: cats
          text: 'Pets, family, or anything else you want visitors to know.'

        - id: travel
          span: 6
          icon: camera
          title: Travel & photography
          art: travel
          text: 'Places, photos, or a link to an album.'

      # Optional visitor map card: shown only when params.yaml → visitor_map.id is set.
      visitors:
        title: 'Visitors'
        text: 'Where readers of this site come from.'
---

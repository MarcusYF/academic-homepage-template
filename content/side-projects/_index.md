---
# Side projects: one wide card per project (layouts/_partials/hbx/blocks/side-projects/block.html). Placeholder content.
title: 'Side Projects'
summary: 'Small tools I build outside my research.'
date: 2024-01-01
type: landing

design:
  spacing: '0'

sections:
  - block: side-projects
    id: side-projects
    design:
      spacing:
        padding: [0,0,0,0]
    content:
      kicker: Side projects
      title: Side projects
      intro: 'Small tools I build to make my own work easier. Personal projects, separate from my research.'
      projects:
        - id: example-tool
          name: Example Tool
          icon: prompter
          status: Preview release · v0.1
          tagline: 'A one-line description of what the tool does and for whom.'
          summary: 'Two or three sentences on the problem it solves and how it works. *(Placeholder.)*'
          features:
            - 'A first feature, described in one line'
            - 'A second feature, with `code` if useful'
            - 'A third feature'
          facts:
            - { label: 'Platform', value: 'macOS, Linux, Windows' }
            - { label: 'Status', value: 'Preview release' }
            - { label: 'License', value: 'MIT' }
          links:
            - { label: 'Download', url: 'https://github.com/your-username/example-tool/releases', icon: download, primary: true }
            - { label: 'Source on GitHub', url: 'https://github.com/your-username/example-tool', icon: code }
        - id: example-demo
          name: Example Demo
          icon: desk
          status: Personal tool
          tagline: 'A project with a screenshot and a link to a demo.'
          summary: 'Add a `preview` image (in static/ or assets/) and a demo link; both are optional.'
          features:
            - 'What a visitor can try in the demo'
            - 'What the real tool does beyond the demo'
          facts:
            - { label: 'Runs', value: 'Locally' }
            - { label: 'Built with', value: 'Your stack' }
          links:
            - { label: 'Read more', url: 'https://example.org/', icon: arrow }
---

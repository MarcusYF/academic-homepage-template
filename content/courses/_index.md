---
# Courses overview (placeholder). Each course is a folder under content/courses/ rendered as a docs page.
title: Courses
summary: Current courses, teaching philosophy and past offerings.
type: landing

cascade:
  - target:
      path: '{/courses/*/**}'
    type: docs
    params:
      show_breadcrumb: true

sections:
  - block: markdown
    id: current-courses
    content:
      title: 'Spring 2026'
      subtitle: 'Example University'
      icon: teach
      text: |-
        ### DS 101: Introduction to Machine Learning

        One or two sentences on the topics, the audience and the format. *(Placeholder.)*

        [Course page](ds-101/) · [Course website](https://example.org/)

        ### DS 520: Algorithms and Society

        One or two sentences on the topics, the audience and the format. *(Placeholder.)*

        [Course website](https://example.org/)
    design:
      columns: '1'
  - block: markdown
    id: teaching-philosophy
    content:
      title: 'Teaching philosophy'
      icon: light-bulb
      text: |-
        A short statement of how you teach. *(Placeholder.)*

        - **A first principle.** One sentence on what it means in your classroom.
        - **A second principle.** One sentence, with an example of an activity.
        - **A third principle.** One sentence on how you assess it.
    design:
      columns: '1'
  - block: markdown
    id: past-courses
    content:
      title: 'Past offerings'
      icon: archive-box
      text: |-
        - DS 101, Spring 2025
        - DS 520, Fall 2024
    design:
      columns: '1'
---

# Project Shore – Architectural Discussion

## Purpose

**Project Shore** aims to be a modular, extensible Django platform for self-publishing authors, featuring surveys, polls, newsletters, reviews, payments, and rich content delivery. This document captures the architectural options and recommendations for building a flexible, future-proof “Survey Builder” that leverages both the `polls` and `surveys` apps.

---

## Architectural Options

### 1. **Combine `polls` and `surveys` Into a Single App**

#### Pros
- Simpler codebase; no duplicated models like `Question` or `Choice`.
- Admin and relationships live in a single namespace.

#### Cons
- Less modular; hard to reuse polls as a standalone feature elsewhere.
- Reduced separation of concerns; all logic lives together.

#### Best for:
- Projects focused entirely on surveys, where polls are just a question type or section.

---

### 2. **Keep `polls` and `surveys` Separate, But Link Them**

#### Pros
- Preserves modularity and separation of concerns.
- `polls` remains a generic toolkit; `surveys` acts as a composer/aggregator.

#### Cons
- Slightly more verbose relationships and imports.
- Slight extra wiring when connecting objects.

#### Best for:
- Projects wanting reusability and clean division of responsibilities.

---

### 3. **Abstract the “Card” or “Section” Concept (Polymorphic Approach)**

#### Approach
- Introduce a `Card` (or `Section`) model in `surveys`.
- Each Card can point (via ForeignKey or Django’s GenericForeignKey) to any content object—Poll, InfoBlock, CustomForm, etc.
- Surveys become ordered sequences of Cards, allowing future expansion to new display objects.

#### Pros
- Maximum flexibility: any kind of “block” or interactive content can be plugged in.
- Easy to add new card types (Contact Info, Images, Custom Forms, etc.) later.

#### Cons
- Slightly more complex initial setup (polymorphism or content types).
- May be more power than needed if only polls/questions are required.

#### Best for:
- Future-focused projects expecting to grow survey/card types over time.

---

## Concrete Recommendation for Project Shore

- **Short-term:**  
  Keep `polls` and `surveys` as separate apps. In `surveys`, create a `Card` (or `Section`) model that links to Polls (or other objects) as its payload.
- **Long-term:**  
  When you want to add more types of cards (Info, Image, Review, etc.), refactor the Card model to use Django’s GenericForeignKey or a similar polymorphic pattern. This enables plugging in any display/content type as a survey step or section.

### Polymorphic Card Model Example

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Card(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='cards')
    order = models.PositiveIntegerField(default=0)
    # Generic relation to any display object (Poll, InfoBlock, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']

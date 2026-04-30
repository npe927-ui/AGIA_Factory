---
titulo: "Chain of Thought Prompting: Prompt Engineering with Chain of Thought for ChatGPT 4"
autor: "Chalk, Edward"
anio: 2024
idioma: "en"
categoria: "negocios"
fuente_original: "Chain of Thought Prompting_ Prompt Engineering with Chain of -- Chalk, Edward -- 2024 -- f6d930184f75e1a92b7e2979d66a89c1 -- Anna’s Archive.epub"
isbn: null
---

Title: Chain of Thought Prompting

Author: Edward Chalk

Publication Date: 03/03/2024

ISBN: 9798322860051

Categories:

- Computers & Technology › Computer Science › Artificial Intelligence › AI & Semantics
- Computers & Technology › Computer Science › Artificial Intelligence › Neural Networks
- Computers & Technology › Applications & Software › Natural Language Processing

Publisher: Self-Published via Amazon KDP

Copyright © 2024 by Edward Chalk

Contact the author for permission requests: edward@fleetingswallow.com

First Edition

Disclaimer:

The information in this book is provided "as is" and the author disclaims all warranties, express or implied, including without limitation any warranties of accuracy, reliability, and any implied warranties of merchantability, fitness for a particular purpose, and non-infringement. The author assumes no liability or responsibility for any errors or omissions in the content of this book.

Amazon KDP Publishing Notice:

This book was self-published via Amazon Kindle Direct Publishing (KDP). Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.

Library of Congress Cataloguing-in-Publication Data

Names: Chalk, Edward, author. Title: Chain of Thought Prompting / Edward Chalk. Description: First Edition. | Includes bibliographical references and index. Identifiers: ISBN 9798322860051 (paperback) Subjects: LCSH: Artificial Intelligence. | Machine Learning. | Computer Science. Classification: LCC Q334.7 .C43 2023 | DDC 006.3--dc23

---

Table of Contents

Foreword

The Dawn of AI

Chain of Thought

Structure of this Book

ChatGPT 4

Join the Conversation

Section I - General Problem Solving Overview

Chapter 1. Adaptive Thinking

Human Versatility

Contextual Adaptability in AI

Limitations of AI Contextual Adaptability

Chapter 2. Hard and Soft Problems

Hard Problems

Soft Problems

Chapter 3. Types of Hard Problems

Conceptual and Empirical Problem-Solving

Types of Conceptual Problems

Types of Empirical Problems

Quantitative Problems

Chapter 4. Combined Hard Problem Types

Systems Analysis

The Hard Sciences

Algorithmic Problems

Chapter 5. AI's Unique Problem Solving Capabilities

Using AI to Solve Quantitative Problems

Generative AI's Unique Capabilities

Chapter 6. Types of Soft Problems

Chapter 7. Using AI to Identify Problem Types

A Day in the Life of a Robot

A Problem Classification GPT

Chapter 8. Framing Problems

Real-World Problems

Reducing Energy Consumption

Framing Hard Problems using AI

A Call-centre Wait Time Problem

A Manufacturing Plant Sustainability Problem

Framing Soft Problems

Section II - Solving Hard Problems

Chapter 9. Problem Solving Methods

Solving Hard Problems

Getting Lift in AI Responses

Chapter 10. Analytical Thinking

Thinking

Further Reading

Chapter 11. The Power of Custom GPT's

Custom GPT's

Improved Reasoning Abilities

An Analytical GPT

The Corporate Safe Challenge

Chapter 12. Solving Causal Problems with CoT Prompting

Introduction to Business Processes

Basic Ideas of a Business Process

Actions, Inputs and Outputs

Chapter 13. CoT Prompting using Business Process Analysis

Casting Causal Problems as a Business Process

The Hugging Face GAIA Dataset

Finding Nemo

Finding a University

Conclusion

Chapter 14. Introduction to Systems Thinking

The Definition of a System

Examples of Systems

Chapter 15. Systems Analysis

Understanding the System as a Whole

Understanding Component Elements

Component Interaction

System Layout

Operational Rules

System Constraints and Feedback Loops

Chapter 16. CoT Prompting with Systems Analysis

Using AI in Classical Systems Analysis

Casting General Problems as Systems Problems

Solving a Logic Puzzle

Solving a Business Problem

Conclusion

Section III - Copying the Experts

Chapter 17. Expert Personality Simulation

Simulating Personalities with ChatGPT

Different Ways of Thinking

Chapter 18. Applying Specific Thinking Styles using AI

Chapter 19. Combining Thinking Styles

Chapter 20. Invoking Specific SMEs (Subject Matter Experts)

Chapter 21. A Subject Matter Expert GPT

Section IV - Introduction to Psychoanalysis

Chapter 22. Combining Psychoanalysis with AI

Psychoanalysis

Simulating the Human Mind using AI

Chapter 23. Introduction to Transactional Analysis

Suitability of Transactional Analysis for Generative AI

Main Areas of Transactional Analysis

Further Reading

Chapter 24. Structural Psychoanalysis

Ego States

Cathexis

Favourite Ego States

Chapter 25. Transactional Analysis (proper)

Complementary Transactions

Crossed Transactions

Dual Level Transactions

Chapter 26. Second Order TA Structural Analysis

Sub-Ego-States

Chapter 27. Intra-Psyche Communication Channels

Channels of Communication

Section V - Psychoanalysis using AI

Chapter 28. Performing Structural Analysis using ChatGPT

Structure of the Psyche

Psychoanalysing the Beatles

Practical Applications of AI Structural Analysis

Chapter 29. Performing Transactional Analysis (proper) using ChatGPT

Analysing Spam Email using Transactional Analysis (proper)

Real Time Transactional Analysis

Section VI - Synthesizing the Human Mind

Chapter 30. Synthesising Ego States using AI

Synthesising Ego State Activity

Choosing a Preferred Ego State Response

Conclusion

Chapter 31. Consulting with Yourself using CoT Prompting

Simulating Internal Thought

Walking The Lairig Ghru

A Holiday in the USA

Python Code

Summary

Chapter 32. A TA Based Product Recommendation Engine

Current Product Recommendation Engines

Designing a Product Recommendation Engine Using an LLM

Specificity of Experience

TA Based Recommendation Method

Worked Example

Section VII - Revisiting Systems Analysis

Chapter 33. Classical Systems Analysis

Implementing Ideas

Limitations of Classical Systems Analysis

Bridging the Gap

Chapter 34. Conceptual Systems Analysis

Triadic Systems Analysis

Triadic Element Interaction

Finding the System Sweet Spot

Chapter 35. Systems Analysis of Transactional Analysis

Chapter 36. Ego-state Specialisation in Systems Analysis

Urban Planning

Healthcare System

Chapter 37. Problem Decomposition

Real World Problems

AI's Need to Decompose Complex Problems

Different Approaches to Measuring Problems

Stakeholder Consensus Analysis

Expansion of Heathrow Airport

Stakeholder Consensus Analysis  in combination with Transactional Analysis

Waking up a Robot's Owner

Chapter 38. Simulating the Human Decision-Making Process

Epilogue

Using CoT Prompting Methods in Combination

Programming AI

Final Thoughts

Appendix A

List of Prompt Engineering Techniques

Appendix B

Comparing CoT Prompting with Classical Prompt Engineering

Basic Principles of Prompt Engineering

Widening the Knowledge Gap

Counterpoints

Demanding Precision

---

# Foreword

## The Dawn of AI

We are currently at the start of a new age in IT, the age of AI. Bill Gates has described the invention of generative AI as revolutionary as personal computers, mobile phones, and the Internet.

As with the start of all technological revolutions, what is happening currently in the world of AI is a process of experimentation and discovery. The aim of this book is to explore this new frontier, and to become a part of this technological revolution.

## Chain of Thought

Currently, most interactions with ChatGPT are done in a simple "one-shot" way. The user provides one input, such as a question, and the AI gives a single output.

There are significant drawbacks to this simple way of using AI:

a)Transparency: We don't know why the AI said what it said, since we can't see the training data that made the AI give that specific response.

b)Processing power: The processing power that the AI allocates to answering one question is limited to the processing power limits imposed by the company that provides it. If determining the correct answer requires more processing power than allocated, the AI will always give the wrong answer.

c)Control: There is no way to control the way that the AI processes the initial question. In other words, it is impossible to guide the way that the AI thinks about the best way to provide an answer.

Another reason to think that this is not the best way to use AI is that it is not the way that we ourselves think and solve problems.

When we are presented with a complex problem, we first break the problem down into discrete steps, and then we solve each step to arrive at the correct conclusion. In other words, we follow a chain of thought. However, when an AI is presented with a problem and is expected to arrive at the solution "in one go", it is not given the opportunity to break down its own thinking processes into discrete steps, before solving the problem.

Therefore, instead of expecting an AI to magically give us the right answer to anything we ask it, it may instead be necessary to engage with AI in multiple problem-solving steps and guide the AI on the correct path to complete its task.

That means, we can use Chain of Thought Prompting to guide the AI in creating its own chain of thought, and so simulate the human problem-solving process. By doing this we can unlock the true potential of a generative AI such as ChatGPT, and demonstrate that its abilities extend well beyond those which are obvious at first sight.

|  | CoT Prompting is an abbreviation of Chain of Thought Prompting . |
|---|---|

## Structure of this Book

This book is divided into the following sections:

- Section I (General Problem Solving Overview) explains how people solve problems, and discusses how these problem-solving methods can be applied by AI.

- Section II (Solving Hard Problems) delves into using CoT Prompting to solve "hard" problems, that is questions which relate to factors in the real-world.

- Section III (Copying the Experts) explores using AI's ability to boost its problem solving capabilities by simulating responses from people who are experts in the problem domain.

- Section IV (Introduction to Psychoanalysis) provides a high level introduction to psychoanalysis and discusses the possibility of using AI to simulate the inner workings of the human mind.

- Section V (Psychoanalysis using AI) uses ChatGPT 4 to perform psychoanalysis.

- Section VI (Synthesizing the Human Mind) uses a combination Transactional Analysis theory and ChatGPT to synthesize patterns of human thought.

- Section VII (Revisiting Systems Analysis) takes a new look at systems analysis in a way that is more suitable for the way that AI processes information.

## ChatGPT 4

The theory presented in this book applies to generative AI in general, however the worked examples in this book use ChatGPT 4. This is because ChatGPT 4 follows instructions accurately, as opposed to other generative AI platforms that often ignore instructions and "do their own thing".

## Join the Conversation

Join the discussion on LinkedIn (linkedin.com/groups/9586057/), or email me at edward@fleetingswallow.com.

Thank you for reading this book, I hope it repays your interest.

Edward Chalk

---

# Section I - General Problem Solving Overview

Discusses general principles of human problem-solving and how these principles can be applied by AI.

This image shows Talos, the first mythical automaton, patrolling a beach. Forged by Hephaestus, Talos was a bronze giant tasked with protecting Crete from invaders. Created by Bing.

---

# Chapter 1. Adaptive Thinking

## Human Versatility

Humans are good at solving all sorts of different problems that come their way in everyday life and at work. This is because they are versatile in their approach to solving problems and adapt their problem-solving approach to suit the challenge at hand.

This adaptability is called adaptive thinking.

|  | Adaptive thinking is the human capacity to assume the mode of thinking that is best suited to solve the immediate problem, and so achieve the optimum outcome. |
|---|---|

## Contextual Adaptability in AI

It follows that if we have to adjust our thinking mode to suit the problem at hand, then AI must also be trained to do the same thing, if we want it to reach the optimal conclusion. A generative AI model (such as ChatGPT) does this automatically, to a limited extent. This means that the AI automatically adjusts its mode of reasoning, depending on the question asked.

AI works this way because the training data that the AI references in order to answer the question, not only includes the information needed to answer the question, but also includes the sort of thinking needed for that type of question.

For example:

- If an AI is asked to answer a maths question, it references training data that contains both the actual mathematical information that the AI needs to answer the question, and also the patterns of thinking used in mathematics.

- On the other hand, if an AI is asked to write a poem, then the AI shifts to a less methodological approach by referencing free-style training data that contains information about poetry, and also the loosely structured patterns of thought of the creative arts.

This AI flexibility is called Contextual Adaptability, which means that the AI adjusts its mode of response based on the query's context.

## Limitations of AI Contextual Adaptability

Although a generative AI such as ChatGPT 4 attempts to adjust its thinking mode to suit the question, there are limitations to this capability, for the following reasons.

- Limited input : The AI may have difficulty in fully understanding the type of problem it's facing. This is because humans use a mixture of contextual cues, prior knowledge, and intuitive understanding to classify problems and decide on the best approach. AI, however, can only go on the text in which the user asked the question.

- Limitations of NLP : The AI may also not exactly grasp nuances in the way it is being asked a question, due to limitations in its NLP (Natural Language Processing) capabilities, and its inability to decode the exact communication style of the questioner.

Subsequently, we need to actively encourage the AI by specifying the type of thinking required, to match the problem we are presenting it.

A robot that can't quite understand a question asked by a human, by ChatGPT

# Chapter 2. Hard and Soft Problems

The first decision we make when faced with a real-life problem is deciding whether we have a hard problem or a soft problem on our hands. These two different types of problems require entirely different problem-solving approaches.

## Hard Problems

The term hard problem as used here does not mean that the problem is difficult to solve. Instead it means that we are talking about a problem that can be exactly defined; "Is it true, or is it false?".

- Hard problems generally relate to the external world, and include physical, technical or data-driven issues.

- Solving hard problems requires exact methods, logical reasoning and accurate data.

- The answers to hard problems are specific, precise and measurable.

## Soft Problems

Soft problems are problems that cannot be exactly defined. They relate to qualitative problems or personal questions such as opinions, emotions and relationships; "Is it good, or is it bad?"

- Soft problems often occur in relation to the human condition; for example in fashion design, in organisational behaviour and in personal decision-making.

- There is often not one correct single answer to soft problems. Instead solving soft problems involves subjective judgment, emotional intelligence and an understanding of human behaviour.

- Solutions to soft problems tend not to be clear-cut and require a nuanced subtle approach to balance the competing needs of human complexity.

| Magical thinking occurs when a person misidentifies a hard problem as a soft problem. In this case they may think that they can make the problem “go away” by applying soft-problem solving methods, which is incorrect. The term “ being hard-headed ” refers to the ability to correctly identify a hard problem as a hard problem, which must be addressed with rigorous, not wishful, thinking. |
|---|

Many scenarios necessitate addressing both hard and soft problems, for instance:

- Implementing a new IT system involves the hard problem of development and deployment and the soft problem of change management.
- Developing a luxury product requires first defining what customers are likely to be attracted to, and then engineering and manufacturing the required product.

Computer systems in a luxury car, bbc.co.uk

---

# Chapter 3. Types of Hard Problems

## Conceptual and Empirical Problem-Solving

| The word empirical refers to knowledge or methods based on observation, experience, or experimentation rather than theory or pure logic. In the context of problem solving, empirical means relying on real-world data to draw conclusions. |
|---|

Generally speaking, within the category of hard problems, we can identify two further general categories, based on the approach used to solve the problem.

- Conceptual problem-solving : These are scenarios where the main thrust of finding a solution to the problem comes through thinking and the intellect.

- Empirical problem-solving : These are scenarios where the problem solving approach is primarily based on real-world data.

These categories serve as umbrella terms, under which we can further identify specific problem types.

## Types of Conceptual Problems

Types of hard problems that are mainly solved through thinking include:

- Analytical Problems : These involve dissecting a problem into smaller parts, addressing each component individually, and then synthesizing an overall solution.
- Causal Reasoning Problems : Solving these problems requires tracing a chain of cause and effect, from the initial cause to the final outcome.

Causal reasoning problems can range from simple "A leads to B" scenarios to complex chains of events involving multiple steps and interactions between various factors.

| Causal reasoning relates to the fundamental idea of cause and effect , and involves identifying the factors (causes) that lead to certain outcomes (effects). For example, if a car won't start, we use causal reasoning to investigate the possible reasons behind the issue, such as a flat battery or an overheated engine, to find a solution to the problem. |
|---|

- Theoretical Problems : These problems relate to the understanding and development of theoretical frameworks and require abstract thinking and mathematical modelling to solve them.

## Types of Empirical Problems

Types of hard problems whose solutions are based on facts include:

- Technical Problems : Involving the repair or creation of technological systems, these problems demand specific technical knowledge and skills, from fixing a washing machine to engineering spacecraft components.

Solving technical problems requires an understanding of the relevant technology and the ability to apply practical skills and innovative thinking to create, fix, or improve technological solutions.

- Methodological Problems : Developing new techniques or tools to study the natural world or improve experiments, such as inventing new instruments or computational methods.

## Quantitative Problems

Maths is an essential skill required to solve the quantitative problems (problems based on numbers) that can arise in all hard-problem areas.

- For conceptual problems , maths provides the framework for developing theoretical models that can predict outcomes, propose new theories, and explore the implications of various hypotheses.

- On the other hand, in empirical problem-solving , maths is needed for designing experiments, analysing data, and interpreting results. It allows researchers to quantify observations, apply statistical tests, and draw reliable conclusions based on empirical data.

Mathematics forces problem-solvers to ensure that their solutions are both theoretically sound and can also be independently verified.

[Imagen: Studying... | An old picture from, I think, when I was study… | Flickr]

Maths, Flickr

---

# Chapter 4. Combined Hard Problem Types

Real-world problems often require the combination of various thinking styles, three examples are presented in this chapter.

## Systems Analysis

Systems problems demand an understanding of how different components interact within a system to produce a holistic result that is greater than the sum of its parts.

Systems thinking requires:

- Understanding the behaviour of each element in the system,

- understanding how the elements interact with each other, and

- understanding how the overall system behaves as a whole.

Examples of system thinking problems occur in software systems development, environmental conservation, organisational change management, public health management and urban planning. In all these cases, we need to understand the behaviour of the system as a whole, the behaviours of all the component elements of the system and their interactions with each other.

Systems analysis includes both conceptual problem-solving and also empirical problem-solving.

This is because, at a high level, a system represents the embodiment of an idea or concept. Therefore from a high level perspective, conceptual problem-solving is required to understand the initial idea, how the idea is represented in the system, and how the system's output corresponds to the initial thinking behind the system.

On the other hand, empirical methods are needed to observe, measure, and manipulate the system's working parts, in real-world applications.

## The Hard Sciences

The hard sciences includes areas of study such as physics, chemistry, biology and mathematics. Within the hard sciences, a range of different types of problems can be encountered, which require specific problem-solving strategies.

The following types of problems are common within the hard sciences.

- Empirical problems require observation, experimentation, and data collection to solve. These problems are grounded in the physical world and often require the formulation of hypotheses, which are then tested through experiments or observational studies.

- Theoretical problems involve the development or refinement of scientific theories to explain empirical observations. These problems require abstract thinking and the application of mathematical models to describe the natural world.

- Computational problems in the hard sciences involve using algorithms and computational models to solve scientific questions.

- Methodological problems involve the development of new techniques or tools to study the natural world. These can include the invention of new instruments, the improvement of experimental procedures, or the creation of novel computational methods.

Solving methodological problems enables scientists to make new discoveries and to measure phenomena with greater accuracy and precision. For instance, developing a more sensitive telescope allows astronomers to observe distant galaxies, while creating a more accurate time-measurement tool can enhance the precision of experiments in physics.

Interdisciplinary problems sit at the junction of multiple scientific disciplines and require a synthesis of concepts and methods from each to be solved. These problems reflect the complexity of the natural world, which does not adhere to the boundaries defined by academic disciplines.

Examples of interdisciplinary problems include understanding the brain's functioning, which requires knowledge from biology, chemistry, psychology, and computer science; or tackling climate change, which involves insights from environmental science, computer science, physics, chemistry, and economics.

Many of the great scientific challenges are comprised of interdisciplinary problems. This is why a scientist may have to apply a number of the above problem solving techniques in order to achieve a true scientific breakthrough.

U.S. supercomputers for weather and climate forecasts, National Oceanic and Atmospheric Administration, U.S. Department of Commerce

---

## Algorithmic Problems

This category includes problems that are addressed through the application of computer code or manual algorithms. Algorithmic problem-solving is a hybrid area that intersects with both conceptual and empirical problem-solving approaches, depending on the nature of the problem and the data involved.

The essence of algorithmic problem-solving lies in its systematic approach to tackling challenges by breaking them down into smaller, more manageable parts, each of which can be addressed through specific, logical steps.

Types of Algorithmic Problems include:

- Classic Computational Problems : Tasks that are inherently suited to computation, such as sorting lists, searching databases, or optimizing routes.

- Data-Driven Problems : With the advent of cheap access to reliable databases, many problems now require sorting through vast datasets to find patterns, make predictions, or derive insights.

- Optimisation Problems : These are challenges that seek the best solution from a set of possible solutions, given certain constraints or criteria. Examples include scheduling tasks, allocating resources, or designing networks.

- Decision-Making Problems : These problems require evaluating multiple options and making choices based on certain, given criteria.

Almost all programming languages implement the basic types of algorithms, such as sorting algorithms, searching algorithms and recursive algorithms.

These basic types of algorithms provide the building blocks for the more complex and specialised algorithms required by the programmer.

---

# Chapter 5. AI's Unique Problem Solving Capabilities

## Using AI to Solve Quantitative Problems

When we start to consider what type of hard problems we can solve using a generative AI, such as ChatGPT, the conversation veers in the direction of considering what Chat GPT actually does when we ask it a question.

- Is Chat GPT primarily functioning as a useful search engine, which amalgamates data and stops us having to trawl through multiple web pages?
- Or is Chat GPT effectively acting as a "thinking engine" which can work out problems for us?

For example, in the area of technical problems, it's obvious that AI does not have good technical skills. AI is unable to handle tools and intuitively feel its way through carefully crafting a machine component. However, AI can be incredibly useful in finding the right technical information to apply to a particular problem. In this case we can think of AI as an intelligent search engine.

On the other hand, generative AI is very good at solving numerical problems described in natural language, as demonstrated in the following example.

| Problem Statement: The Effect of Introducing a Homework Support Program on Student Performance Scenario Description A local middle school has introduced a new after-school Homework Support Program (HSP) aimed at improving student performance in mathematics. The program provides students with access to tutors, resources, and a structured environment for completing homework. The school aims to evaluate the effectiveness of the HSP in enhancing students' mathematics grades. Objective Determine if participation in the Homework Support Program impacts students' mathematics grades, using a simple before-and-after comparison within participants and non-participants groups. Data Provided Participants : 20 students, with 11 participating in the HSP (treatment group) and 9 not participating (control group). Mathematics Grades : Collected for each student before (pre-program) and after (post-program) the HSP introduction. Data |
|---|
|  | Student ID | Pre-Program Grade | Post-Program Grade | HSP Participant |  |
|  | 1 | 78 | 85 | Yes |  |
|  | 2 | 82 | 88 | Yes |  |
|  | 3 | 74 | 76 | No |  |
|  | 4 | 69 | 72 | No |  |
|  | 5 | 80 | 90 | Yes |  |
|  | 6 | 83 | 87 | Yes |  |
|  | 7 | 75 | 78 | No |  |
|  | 8 | 77 | 79 | No |  |
|  | 9 | 72 | 82 | Yes |  |
|  | 10 | 85 | 91 | Yes |  |
|  | 11 | 70 | 73 | No |  |
|  | 12 | 68 | 70 | No |  |
|  | 13 | 76 | 84 | Yes |  |
|  | 14 | 81 | 85 | Yes |  |
|  | 15 | 73 | 75 | No |  |
|  | 16 | 79 | 80 | No |  |
|  | 17 | 84 | 92 | Yes |  |
|  | 18 | 67 | 69 | No |  |
|  | 19 | 71 | 83 | Yes |  |
|  | 20 | 86 | 93 | Yes |  |
|  |
| Steps for Analysis |
| Calculate Average Improvement : For each group (Yes, No), calculate the average difference between pre- and post-program grades. Compare Averages : Compare the average grade improvement between HSP participants and non-participants to assess the program's effectiveness. Evaluate Effectiveness : Determine if the average grade improvement for HSP participants is significantly greater than for non-participants, suggesting a positive impact of the program on students' performance. |

Solving this problem proves relatively trivial for ChatGPT 4:

Chat link: https://t.ly/FR8cQ

| ChatGPT The analysis of the Homework Support Program's effect on student performance in mathematics yields the following results: The average improvement in grades for students who participated in the Homework Support Program (HSP) is approximately 7.45 points. The average improvement in grades for students who did not participate in the HSP is approximately 2.22 points. These results suggest that participation in the Homework Support Program has a positive impact on students' mathematics grades, with participants experiencing a significantly greater improvement in their grades compared to non-participants. This indicates the effectiveness of the HSP in enhancing students' performance in mathematics. |
|---|

In this case, ChatGPT acts as a "thinking machine", not just as a glorified search engine.

## Generative AI's Unique Capabilities

The truth is however, that AI's ability to solve maths problems is not really the groundbreaking aspect of current generative AI models.

Solving numerical problems is stock-standard in the programming world, and so although AI does add another dimension with automatic code generation and automatic question-analysis using NLP (natural language processing), this is not an altogether unprecedented capability.

Where generative AI really shines is in the realm of qualitative thought, where its abilities to apply human-style logical thinking to analytical problems, causal reasoning problems and systems thinking problems are unprecedented in the world of IT.

Investigating these unique capabilities is the subject of Section II of this book.

---

# Chapter 6. Types of Soft Problems

It is difficult to categorise soft problems according to their essential nature, since by definition soft problems are not well defined. However, we can categorise soft problems according to the way we deal with them:

- Soft Problems that Require a Logical Approach : Types of soft problems that require a logical approach include significant life decisions, goal setting, developing relationships and adapting to change. All these problems require a structured thinking approach to find the best approach and the best way to progress the situation.

- Soft Problems that Require an Emotional Approach: Many of the situations and challenges we are faced with require an emotional approach, involving empathy, understanding, warmth and emotional intelligence.

For example,an emotional approach is needed in developing relationships, achieving personal growth and attaining inner peace and harmony.

- Soft Problems that Require a Control Approach : This category includes scenarios where exerting direction, guidance, and management over one's own behaviour or other people's behaviour is the best way of dealing with the situation.

This approach may be needed to achieve goals, maintain order, and ensuring personal and professional integrity.

Identifying the type of soft problem we are faced with is crucial to crafting a suitable response. For example, adopting a "control" approach to a situation which requires an emotional response is a recipe for disaster, and vice-versa.

Identifying and applying the correct way for an AI to solve soft problems is discussed in Section V, Section VI and Section VII of this book.

---

# Chapter 7. Using AI to Identify Problem Types

The first step in using Chain of Thought Prompting for solving real-world problems is to identify the type of problem with which we are dealing. Once we have done this, we can guide the AI in selecting the right problem-solving approach.

Humans tend to be better than AI at problem-type identification, due to their awareness of the contexts in which problems occur, and their understanding of subtle details which may not be easily explained to an AI in writing. Therefore it may be necessary for the user to guide the AI in understanding the problem type and subsequently the best type of thinking to apply in order for the AI to achieve the optimal outcome.

However, advanced AI models, such as ChatGPT 4, do have the capacity to identify the correct problem-solving approach for specific problems, however.

## A Day in the Life of a Robot

Imagine a domestic help robot that is having a challenging day, in addition to its normal duties, it has to deal with the following issues.

- Unexpected Messes : The robot encounters spills and sudden messes that were not part of its initial cleaning schedule.
- Dynamic Obstacles : The robot has to navigate around pets, children and temporary obstacles that are not usually present.
- Wear and Tear : The robot experiences mechanical issues or software glitches due to regular use, these require diagnostics and maintenance.
- Power Management : The robot has to manage its battery life to complete all tasks without running out of power at inconvenient times or locations.
- Adapting to Changes : The robot has to adjust to new furniture arrangements, renovations, or other changes to the physical layout of the home.
- Complex Instructions : The robot has to interpret and execute complex or vague instructions from humans, which might not always be straightforward or within its programmed capabilities.
- Safety Concerns : The robot has to ensure the safety of all household members, especially children and pets.
- Privacy Issues : The robot has to navigate the need for privacy with the requirement to perform its tasks, especially in areas like bathrooms or bedrooms.
- Communication Challenges : The robot has to communicate with household members, understanding their needs, and conveying information or asking for clarification.
- Decision Making : The robot has to make judgment calls in unexpected situations, like whether to interrupt a sleeping household member for a critical task or how to prioritize conflicting commands from different family members.

## A Problem Classification GPT

Using a custom GPT that is designed to classify problems according to their problem type (Problem Classifier GPT - https://t.ly/GFfUg), let's see how we can classify each of the above problems.

|  | For further information on creating custom GPT’s, see Chapter 11. The Power of Custom GPT’s. |
|---|---|

Shared chat: https://t.ly/dPWke

| You Classify the following problems: Imagine a domestic help robot that is having a difficult day. Problem Classifier The problems described for a domestic help robot involve a mix of technical (hard) and interpersonal/social (soft) challenges. Below is a classification of each problem along with a recommended approach for solving it: Unexpected Messes : This is a hard problem . It requires analytical methods and technical knowledge for the robot to dynamically adjust its cleaning schedule and methods. An effective approach would involve implementing machine learning algorithms that can adapt to unexpected changes in the environment. Dynamic Obstacles : This is a hard problem . Solving it involves systems thinking and technical enhancements to improve the robot's navigation algorithms, enabling it to detect and respond to moving obstacles in real-time. Wear and Tear : This is a hard problem . It necessitates a combination of diagnostics for identifying issues and technical knowledge for maintenance and repairs. Predictive maintenance techniques could be useful here to anticipate failures before they occur. Power Management : This is a hard problem . It requires analytical methods to optimize task scheduling and energy consumption, ensuring the robot can complete its tasks efficiently without running out of power. Adapting to Changes : This is a hard problem . It involves systems thinking to integrate sensors and machine learning algorithms capable of recognizing and adapting to changes in the environment, such as new furniture layouts. Complex Instructions : This is a soft problem with a technical aspect. It requires leveraging technical knowledge to improve natural language processing capabilities and emotional intelligence to better interpret human commands that may be vague or complex. Safety Concerns : This is a soft problem . Ensuring safety involves understanding human behaviour and organizational understanding to prioritize tasks in a way that minimizes risks to household members, especially vulnerable ones. Privacy Issues : This is a soft problem . It requires negotiation and emotional intelligence to balance the need for privacy with the requirement to perform tasks efficiently. Developing guidelines and settings that allow household members to customize the robot's access to private areas can be a part of the solution. Communication Challenges : This is a soft problem . It involves emotional intelligence and organizational understanding to effectively communicate with household members, understand their needs, and seek clarification when necessary. Decision Making : This is a soft problem with a technical aspect. While it involves judgment calls that require emotional intelligence to assess the impact of actions on household members, it also needs analytical methods to prioritize tasks based on an understanding of the household's dynamics and preferences. For hard problems, focusing on enhancing the robot's technical capabilities through machine learning, predictive analytics, and advanced diagnostics is key. For soft problems, developing emotional intelligence, effective communication strategies, and an understanding of household dynamics are crucial. Implementing user-customizable settings and privacy controls can also help address soft problems related to privacy and personal preferences. |
|---|

---

The custom GPT is able to accurately identify the type of problem faced by the robot in each situation. In practice this would mean that the robot's processing centre would then be able to route the problem through the type of processing best suited for that problem type.

The ability to initially identify what the actual problem type is, is a essential precursor for a general purpose AI, such as may be found in a domestic help robot, to accurately and efficiently address the problem at hand.

After breakfast, by ChatGPT

---

# Chapter 8. Framing Problems

## Real-World Problems

In the previous chapter, we discussed classifying the type of a particular problem. However in reality, complex real-world hard problems can be viewed and assessed from different perspectives.

Therefore, when we want to solve real-world problems, we first of all have to decide the type of problem we will consider the problem as, and then choose the right problem-solving method. We can describe this process as framing the problem as a particular problem type.

## Reducing Energy Consumption

As an example of the above idea, we can view the problem of reducing energy consumption in a manufacturing plant in several ways:

- Analytical Problem : In this case the focus is on analysing energy usage by machinery, shifts, and processes, to identify patterns of high usage and target them for improvement.
- Causal Reasoning : Assessing the problem with causal reasoning methods requires identifying the factors that lead to high energy consumption and how they are interlinked.
- Quantitative Challenge : Framed as a quantitative challenge, reducing energy consumption in a manufacturing plant involves a statistical analysis of historical energy-consumption data, forecasting energy consumption trends, modelling the impact of potential interventions and quantifying the expected savings from suggested changes.
- Systems Thinking : A systems thinking perspective requires considering how different elements of the manufacturing plant interact and influence each other, including human behaviour, operational processes and external factors like weather conditions.

- Technical Problem : Framing the issue as a technical problem focuses on the specific technological aspects that contribute to high energy consumption. This might involve identifying outdated or inefficient machinery that needs upgrading or replacement.

Each of these ways of casting the original problem highlights different facets of the same underlying issue--reducing energy consumption--but guides the problem-solving process in a slightly different direction.

In reality, it would be possible to apply all these methods and combine their conclusions. This would guarantee addressing all aspects of the original problem and reaching the optimal conclusion.

## Framing Hard Problems using AI

Because AI models such as ChatGPT 4 are trained on a wide range of problem-solving scenarios, they are capable of determining how to best consider a problem with a high degree of relevance.

The AI does this by recognising patterns in the question being asked, and then looking for analogous patterns in real-world problems that were successfully addressed using a particular problem solving approach.

The following examples show how AI can categorise real-world problems as a particular problem-type. The examples use a GPT specifically designed for problem-type categorisation - Problem Solver Insight (https://t.ly/5uwg2).

| The Problem Classifier GPT used in the previous chapter classifies problems as a specific problem type. The Problem Solver Insight GPT , however, considers various ways in which a problem can be assessed and then decides on the optimal approach . |
|---|

## A Call-centre Wait Time Problem

As an example of using AI to frame a real-world problem in the optimal manner, let's consider the following call-centre wait time problem:

### Problem Statement

During both peak and off-peak periods, the typical wait time for callers to Acme Corporation's customer support exceeds five minutes. This situation stems from insufficient staffing levels, leading to customer service agents being overstretched.

### Background

Acme Corporation is grappling with prolonged customer support hold times, marking a departure from its historical reputation for prompt and efficient service. Factors like inadequate staffing and surging demand from customers have contributed to consistently long wait times, causing customer dissatisfaction and eroding loyalty, which in turn tarnishes Acme's brand reputation.

### Relevance

It is imperative for Acme Corporation to tackle the issue of extended wait times for support calls. These delays negatively affect customer contentment and allegiance, risking increased customer turnover and revenue loss. Moreover, a declining service reputation could have enduring effects on Acme's market competitiveness. Promptly addressing this issue is crucial to enhance the customer experience and uphold a strong brand image.

### Objectives

The main goal of this initiative is to shorten the wait times for Acme Corporation's customer support callers. To achieve this, the project will:

- Examine the existing customer support operations to identify inefficiencies causing extended wait times.

- Evaluate staffing and resource distribution to quantify the impact of staffing shortages on service quality.
- Implement strategies to refine the customer support process and decrease wait times.

- Utilize key performance indicators (KPIs) such as average wait time, customer satisfaction scores, and direct feedback to gauge the success of the improvements made.

- Develop a long-term plan to ensure consistently short wait times, considering both high and low demand periods, through strategic staffing, ongoing training, and process optimization.

The Problem Solver Insight GPT recommended a systems analysis approach for this problem.

Shared chat: https://t.ly/PXzQc

| Problem Solver Insight To effectively address the problem of extended wait times for callers to Acme Corporation's customer support, the recommended approach is a systems analysis approach. Here’s why this approach is most suitable and how it aligns with the objectives you've outlined: Rationale for Systems Analysis Approach Holistic Examination of Operations : Systems analysis allows for a comprehensive examination of the existing customer support operations. It goes beyond looking at surface-level symptoms (long wait times) to understand the underlying causes (staffing levels, process inefficiencies, demand surges). This aligns with your first objective of identifying inefficiencies within the support operations. Quantitative and Qualitative Evaluation : This approach facilitates both quantitative (e.g., staffing levels, call volume) and qualitative (e.g., process flow, customer satisfaction) analyses. It matches your second objective, which involves evaluating staffing and resource distribution to understand their impact on service quality. Strategic Implementation of Solutions : Systems analysis supports the development of informed strategies by considering the interdependencies within the customer support system. This ensures that solutions are not only effective in reducing wait times but also sustainable, addressing your third objective of refining the customer support process. Performance Measurement : This approach emphasizes the importance of setting and monitoring KPIs to evaluate the effectiveness of implemented solutions. It directly correlates with your fourth objective, using average wait time, customer satisfaction scores, and direct feedback as measures of success. Future-proofing Customer Support : Finally, systems analysis promotes the development of adaptable and scalable solutions, ensuring that the customer support system can handle fluctuations in demand. This is essential for achieving your fifth objective of developing a long-term plan to maintain short wait times, considering both peak and off-peak periods. Implementation Insights Process Optimization : Investigate current workflows for bottlenecks and implement process improvements, such as automated call routing and self-service options, to reduce demand on agents. Strategic Staffing : Utilize predictive analytics to forecast demand and adjust staffing levels accordingly. This includes not just hiring more staff but also reevaluating schedules, shift patterns, and the use of part-time or temporary workers during peak times. Training and Support : Enhance agent efficiency and job satisfaction through targeted training and support, improving their ability to resolve calls quickly and effectively. Technology Utilization : Explore technology solutions like AI chatbots or enhanced IVR (Interactive Voice Response) systems to handle routine inquiries, thus freeing up human agents for more complex issues. Continuous Improvement : Establish a culture of continuous improvement, where feedback from both customers and agents is regularly collected, analysed, and used to make further enhancements to the support process. By adopting a systems analysis approach, Acme Corporation can ensure a comprehensive, strategic, and adaptable solution to the problem of extended wait times, leading to improved customer satisfaction and a stronger competitive position in the market. |
|---|

## A Manufacturing Plant Sustainability Problem

Let's try running a different type of problem through the Problem Solver Insight GPT:

### Problem Statement

Sunrise Beverages is aiming to reduce its environmental footprint by 20% within the next three years, focusing on reducing water usage and packaging waste in its production processes. However, the company currently lacks a comprehensive sustainability strategy and faces challenges in inefficient resource use and waste management practices. For Sunrise Beverages to achieve its environmental objectives, it is imperative to adopt more sustainable production methods, enhance waste recycling programs, and engage in water conservation efforts.

Objective
Pinpoint specific practices and areas within Sunrise Beverages' operations that significantly contribute to its environmental impact, then addressing these through targeted interventions.

### Approach

- Assessment of Production Processes : Conduct a detailed analysis of current production operations to identify inefficiencies in water use and waste generation. This step will prioritize areas where interventions could yield substantial environmental benefits.
- Implementation of Sustainable Technologies : Explore and adopt cutting-edge technologies designed to minimize resource consumption and environmental impact. The effectiveness of these technologies will be measured by their ability to reduce water and waste footprints.
- Expansion of Recycling Efforts : Enhance recycling programs by introducing more recyclable materials and forming partnerships that support waste diversion from landfills. The impact of these efforts will be evaluated by their contribution to the overall reduction in packaging waste.
- Water Conservation Initiatives : Implement measures aimed at reducing water consumption, including the installation of efficient water recycling systems. The success of these initiatives will be gauged by their contribution to the company's water usage reduction targets.
- Sustainability Branding and Consumer Engagement : Develop a brand image that reflects the company's commitment to sustainability, aiming to strengthen customer loyalty and attract environmentally conscious consumers. The effectiveness of this strategy will be assessed by changes in consumer perceptions and buying behaviours.
- Resource Allocation for Sustainability Goals : Allocate financial, technological, and human resources to support the identified sustainability initiatives. The allocation strategy will be optimized based on the anticipated environmental return on investment.
- Performance Tracking and Strategy Adjustment : Monitor environmental performance indicators, such as reductions in water use, waste generation, and overall environmental footprint. This monitoring will inform ongoing adjustments to the sustainability strategy, ensuring continuous improvement.
- Long-term Commitment to Environmental Performance : Develop a comprehensive environmental strategy that ensures the company's operations are aligned with sustainability goals over the long term. This strategy will include mechanisms for adapting to new environmental challenges and regulations.

Outcome
By following this structured approach, Sunrise Beverages aims to effectively address its environmental impact, achieving a 20% reduction in its footprint through focused improvements in water and waste management. This strategy not only positions the company as a leader in sustainability but also ensures its resilience and competitiveness in an increasingly eco-conscious market.

In this case, the Problem Solver Insight GPT recommended a combined systems analysis and sequential problem solving approach.

Shared chat: https://t.ly/xq8yp

| Problem Solver Insight The problem presented by Sunrise Beverages requires a multifaceted approach that combines both systems analysis and a sequential, temporal analysis of cause and effect. Here's how each approach would contribute to solving the problem: Systems Analysis Approach Systems analysis is essential for understanding and improving the complex interactions within Sunrise Beverages’ production processes and environmental impact. This approach allows for: Holistic Understanding : By viewing the company’s operations as an interconnected system, you can identify how changes in one area (e.g., water usage) affect others (e.g., energy consumption and waste production). Identification of Inefficiencies : A systems analysis will help pinpoint inefficiencies not just in resource use but also in the production processes, supply chain, and product lifecycle. Integrated Solutions Development : Solutions that arise from systems thinking are inherently comprehensive, addressing multiple aspects of sustainability simultaneously. For example, adopting a technology that reduces water use might also decrease energy consumption and waste generation. Sequential Temporal Analysis A sequential temporal analysis focuses on the cause-and-effect relationships over time, helping Sunrise Beverages to: Prioritize Interventions : Understand the temporal impact of different sustainability initiatives. For example, quick wins like improving recycling can have immediate effects, while technology upgrades may offer long-term benefits. Phased Implementation : Develop a timeline for the rollout of different initiatives, considering how early successes can fund and facilitate later, more ambitious projects. Monitor Progress and Adapt : By evaluating the effects of sustainability initiatives over time, the company can adjust its strategies based on what is most effective, ensuring continuous improvement towards its environmental goals. Recommended Approach A combined approach leveraging both systems analysis and sequential temporal analysis is recommended for Sunrise Beverages. Initially, employ a systems analysis to gain a comprehensive understanding of the company’s current environmental impact and identify key areas for improvement. This should involve mapping out all processes, resources, and outputs to identify inefficiencies and interdependencies. Then, use sequential temporal analysis to plan and implement targeted interventions. This involves: Setting short-term, medium-term, and long-term goals based on the identified priorities. Phasing the rollout of initiatives to ensure early wins can support later projects. Continuously monitoring the impact of these initiatives over time to adapt the strategy as necessary. For example, start with an assessment of current processes to identify quick improvements in water and waste management. Then, gradually implement more significant changes, such as adopting new technologies and expanding recycling programs. Throughout this process, it’s crucial to monitor outcomes, learn from the results, and adjust the approach as needed to meet the environmental objectives. This combined approach ensures that Sunrise Beverages not only addresses its immediate inefficiencies but also develops a sustainable, long-term strategy that can adapt to new challenges and opportunities. |
|---|

As illustrated, ChatGPT is capable of identifying the best way to frame a real-world hard problem, to reach an optimal solution. This means that we can continue by applying the most appropriate method to solve the problem, using Chain of Thought Prompting techniques.

Significantly, this allows us to achieve adaptive thinking in the context of AI, for solving real-world hard problems.

---

## Framing Soft Problems

Unlike hard problems, it is not possible to definitively determine the "type" of a soft problem. Instead it is more likely that any "soft" problem will have various elements interwoven in it, some of which require a logical approach, some of which require an emotional approach and some of which require a "control" approach.

Using Chain of Thought Prompting to address soft problems is addressed in Section III and Section IV of this book.

Finding the right approach, by ChatGPT

---

# Section II - Solving Hard Problems

This section goes into a detailed explanation of using Chain of Thought Prompting to solve real-world problems, by applying the problem solving methods best suited to the specific problem type.

Humans and Artificial Intelligence working together to tackle complex problems, by ChatGPT

---

# Chapter 9. Problem Solving Methods

## Solving Hard Problems

As discussed in the previous section, generative AI models such as ChatGPT 4, excel in addressing the following types of hard problems:

- Analytical Problems : Analytical problems involve dissecting complex issues into manageable parts to find a possible solution.

- Causal Reasoning Tasks : Problems that involve predicting outcomes, based on a series of interconnected events or actions.

- System Thinking Problems : Problems that require understanding how different components interact within a system to produce a holistic result.

Each of these problem types has specific problem-solving methods that have been designed specially for that sort of the problem. The following table lists problem solving methods that can be applied to each of these problem types by using CoT Prompting.

| Problem type | Suitable Problem Solving Method |
|---|---|
| Analytical Problems | Classical Analytical Thinking Traditional, systematic approaches to problem-solving that rely on logical reasoning and analysis, such as deductive and inductive reasoning. Generative AI models like ChatGPT 4 add value to this process by recalling relevant data that adds insights to each stage of the “thinking process”. |
| Causal Reasoning Tasks | Business Process Analysis This problem-solving technique is designed to tackle structured, sequential problems by mapping out processes and identifying potential improvements and likely outcomes. |
| Systemic Thinking Problems | Systems Thinking This approach aims to understand the problem domain as a whole, its constituent elements, and how they interact with each other. |

By applying these problem-solving methods using CoT Prompting we can get the AI to break down its thinking into discrete steps and apply relevant information to each stage of its "thinking process".

## Getting Lift in AI Responses

An active area of current research in AI is the idea of getting lift, which refers to the process of elevating the performance of an AI model by using skilful prompt engineering techniques.

Getting lift is essential in the ongoing development of AI technologies. As LLM's grow larger and larger, we encounter physical limits to how LLM models can become, dictated by factors such as available computational resources, energy consumption, and the efficiency of model architectures.

Getting lift through advanced prompt engineering, such as Chain of Thought (CoT) Prompting, is an innovative way to maximise the potential of existing LLM models without the need for scaling their size exponentially.

In the following chapters a focus is placed on demonstrably getting lift in AI responses.

---

# Chapter 10. Analytical Thinking

## Thinking

Generally speaking when we use the word "thinking", we are referring to analytical thinking.

Analytical thinking simplifies complex problems by breaking them down into more manageable parts. It involves pinpointing and dissecting the issue, collecting relevant information, and considering the problem and relevant data logically to come to a solution.

Specific types of analytical thinking include:

- Deductive reasoning : Going from a general theory to specific cases.

- Inductive reasoning : Starting with specific observations, then leading to generalisations.

Analytical thinking is vital for everyday decision-making and for the application of professional skills.

## Further Reading

It would not be possible to explain the foundations of analytical thinking in one book, since a vast body of literature is dedicated to explaining these concepts.

Some key works are as follows.

Classical Texts and Philosophical Works

- Prior Analytics, by Aristotle : This is one of the earliest texts on logic and reasoning. Aristotle explores deductive reasoning and syllogism, which are foundational to analytical thought.

| A syllogism joins two or more premises to arrive at a conclusion. The structure of a syllogism ensures that if the premises are true and the argument is structured correctly, the conclusion must also be true. The classic example of a syllogism is: Major premise : All humans are mortal. Minor premise : Socrates is a human. Conclusion : Therefore, Socrates is mortal. Syllogisms have been key in philosophical, mathematical, and legal reasoning for many centuries. |
|---|

- Discourse on Method, by René Descartes : Descartes outlines his method for achieving clear and certain knowledge, emphasising doubt, analysis, and systematic reasoning as tools for intellectual inquiry.
- Critique of Pure Reason, by Immanuel Kant : Kant examines how we understand the universe through our senses and reason.

Modern Books on Critical Thinking and Analysis

- Thinking, Fast and Slow, by Daniel Kahneman : Kahneman explores two modes of thought: fast, intuitive thinking, and slow, analytical reasoning.

- The Demon-Haunted World: Science as a Candle in the Dark, by Carl Sagan : Sagan promotes scientific scepticism and the use of analytical thinking to overcome vague understanding and pseudoscience.

- Critical Thinking: A Concise Guide, by Bowell and Kemp : This is a practical introduction to critical thinking, covering essential skills, arguments, fallacies, and the importance of reasoning in a clear and accessible way.

---

Texts on Logic and Scientific Method

- The Logic of Scientific Discovery, by Karl Popper : Popper discusses the philosophy of science and introduces falsifiability as a criterion for distinguishing scientific theories from non-scientific ones.

- An Introduction to Logic, by Copi, Cohen and McMahon : This textbook provides a comprehensive overview of logic, including syllogisms, fallacies, and the principles of sound reasoning.

Mathematics and Problem Solving

- How to Solve It, by George Pólya : Pólya presents a systematic method for solving mathematical problems and also emphasises a general approach to problem-solving that applies beyond mathematics.

Together, these classical texts offer a blend of theoretical frameworks, practical insights, and methods for gaining clear analytical thinking.

Kant observing the universe, by ChatGPT

---

# Chapter 11. The Power of Custom GPT's

| This chapter digresses from the subject of CoT Prompting to discuss the potential of custom GPT’s in classical problem solving. |
|---|

ChatGPT 4 displays relatively good analytical thinking capabilities out-of-the box, let's see if we can improve on its native capabilities, however.

## Custom GPT's

In November 2023, OpenAI released the capability for users to create their own custom GPT's. Custom GPTs work better for specific applications than general ChatGPT models, for the following reasons.

- Tailored Data and Specialised Knowledge : Custom GPT models can be fine-tuned on specific knowledge datasets. This means the model can be trained to understand and generate text that is highly relevant to a particular domain or industry.

For example, for industries or applications requiring specialised knowledge, such as legal, medical, or technical fields, a custom GPT model can be trained on technical and industry texts that cover the knowledge areas required by users.

- Enhanced Contextual Understanding : Custom models can be fine-tuned to look out for specific conversational contexts or user needs, and so provide responses that are more relevant and useful in particular scenarios.

For example, a model targeted at customer support can handle queries in a more professional and friendly way than the standard ChatGPT model.

In this way, custom GPT models allow for personalised and domain specific interaction and so bridge the gap between general AI capabilities and specialised industry-specific requirements.

## Improved Reasoning Abilities

A not generally appreciated fact is that in addition to the above capabilities custom GPT models can also display superior reasoning abilities. This is because they can be trained on texts that contain the patterns of talking and thinking which are best suited for a particular type of question.

For example, a custom GPT model trained on legal documents, case studies, and legal theory will not only understand the terminology and concepts used in the legal domain but will also be able to apply legal-style reasoning to analyse situations, draw conclusions, and provide advice in a way that mirrors the reasoning of legal professionals.

This improved reasoning ability provides us with a powerful tool to gain enhanced logical processing power for specific question types.

## An Analytical GPT

As an example of this enhanced reasoning ability, we'll use a GPT called Analytical Thinker GPT (https://t.ly/NJmwZ).

Interestingly, this GPT was not provided with any extra texts when it was created. It is simply a GPT that was designed to apply the thinking methods described in the classical analytical thinking texts to the problems it is asked. Amazingly, it still outperforms standard ChatGPT 4.

Let's use this GPT to solve a logic puzzle, and compare the custom GPT's output to standard ChatGPT 4.

---

## The Corporate Safe Challenge

Consider the following logic puzzle:

### Background

A multinational corporation has secured its most valuable contracts and patents in a state-of-the-art safe. This safe requires five unique codes to open, each held by a different executive (CEO, CFO, CTO, COO, and CMO). To ensure the security of these documents, the codes must be entered in a specific sequence based on a set of logical rules.

### Logical Rules

- The CEO's code must be entered either first or last.
- The CTO's code cannot be entered directly after the CFO's or directly before the COO's.
- The CFO's code must be entered immediately before the CMO's.
- The COO's code is to be entered at some point before the CMO's code, not necessarily immediately.
- No executive's code can be entered twice.

### Objective

Determine the sequence in which the codes should be entered to unlock the safe.

### Solution Approach

To solve this logic puzzle, follow these steps:

- List all executives : CEO, CFO, CTO, COO, CMO.
- Apply Rule 1 : CEO's code is first or last.
- Apply Rule 3 and 4 together : Since the CFO's code comes immediately before the CMO's, and the COO's code comes before the CMO's, it places the CFO and CMO towards the end but not necessarily at the very end, considering the CEO's position and the COO's position relative to the CMO.
- Apply Rule 2 : The CTO's placement is restricted by the CFO and COO's codes. It cannot follow the CFO immediately or be immediately before the COO, helping narrow down its position.
- Logical Deduction : Using the above rules, deduce the only sequence that satisfies all conditions.

### Determining the Sequence

- Start by placing the CEO, considering Rule 1.
- Integrate the placement of CFO and CMO based on Rule 3.
- Consider where the COO can fit, which must be before the CMO but not necessarily right before, as per Rule 4.

Find the suitable spot for the CTO, adhering to Rule 2's restrictions.

ChatGPT 4 becomes confused if we ask it to solve this problem and does not come to a conclusion.

| You solve: The Corporate Safe Challenge Background: A multinational corporation ... ChatGPT To solve "The Corporate Safe Challenge" logically, let's break down the requirements and constraints step by step and then deduce the sequence in which the codes should be entered. 1. List all executives: CEO, CFO, CTO, COO, CMO. 2. Apply Rule 1: The CEO's code is either first or last. This gives us two major scenarios to consider . 3. Apply Rule 3 and 4: Since the CFO's code must come immediately before the CMO's, and the COO's code must come before the CMO's (but not necessarily immediately), we know the sequence involves CFO->CMO, with the COO placed somewhere before the CMO. This also implies the COO cannot be last. 4. Apply Rule 2: The CTO's code cannot follow the CFO's immediately or be placed right before the COO. This rule helps in placing the CTO with respect to the CFO and COO's positioning. Determining the Sequence: Scenario 1 (CEO First): If the CEO's code is first, the sequence starts with CEO. Given the CFO must precede the CMO and the COO must precede both but not necessarily directly, the CTO's placement becomes crucial. Scenario 2 (CEO Last): If the CEO's code is last, we must arrange the other four with the constraints in mind, ending with CEO. Logical Deduction: The COO cannot be last because the CMO must be preceded directly by the CFO, and the COO must come before the CMO. The CTO cannot be placed directly after the CFO or right before the COO, limiting its position. Given these rules, let's construct the sequence with logical deductions: CEO First Scenario: CEO, _, _, _, _. ➢ Since the CFO must come immediately before the CMO and the COO must come before the CMO, and considering the CEO is first, the latter part of the sequence might involve the COO before CFO and CMO. The CTO's restrictions with the CFO and COO mean it cannot be placed between CFO and COO or directly after the CFO. ➢ The sequence could potentially be CEO, CTO, COO, CFO, CMO, but this violates the rule that the CEO should be first or last and does not fit all conditions perfectly, especially considering the placement of the CTO. CEO Last Scenario: _, _, _, _, CEO. ➢ This setup allows us to place the CFO and CMO towards the end of the sequence, preceded by the COO, and then fit the CTO where it doesn't violate its restrictions. ➢ The logical sequence, considering all rules, would be: CTO, COO, CFO, CMO, CEO, which fits all the given conditions. However, this arrangement does not satisfy the CEO being either first or last with the correct placement of other executives based on the provided rules. Correct Sequence Deduction: Given the constraints and revising the approach: CEO cannot be the second or fourth, as it restricts the placement of other roles too much. The CTO’s placement is key, given its restrictions around the CFO and COO. Given the misstep in the initial logical deduction, let's correct the approach: CEO Placement: CEO must be first or last. CFO and CMO Link: They must be consecutive. COO Before CMO: COO must precede CMO but isn't directly linked to being right before CMO or CFO. CTO's Restrictions: It cannot be immediately after CFO or right before COO, which is a critical point to place CTO correctly. Revised Logical Placement: Considering the CEO's flexible placement and the direct link between CFO and CMO, along with COO's precedence over CMO but not directly, we focus on fitting the CTO without violating its restrictions. Given the CTO's placement is highly restrictive, it logically fits in positions not directly after CFO nor before COO in a sequence that doesn't violate the CEO's positioning rule. To accurately solve this with a step-by-step logical deduction, let's construct a sequence satisfying all rules: CEO Placement: Start with CEO at the beginning or end. Fitting CFO, CMO, and COO: CFO and CMO must be together; COO must precede CMO. CTO Placement: Ensure it doesn't follow CFO directly or precede COO directly. Correct Solution: Given the complexity and the need to satisfy all conditions, let's simulate the logical deduction process to find the exact sequence. I'll now solve this logically through deduction based on the constraints provided: CEO's position is pivotal; it dictates the structure. CFO directly before CMO places these two in a linked sequence. >> Continue generating |
|---|

Now let's ask the Analytical Thinker GPT (https://t.ly/NJmwZ) to solve the puzzle; it immediately arrives at the correct answer.

Shared chat: https://t.ly/6I60X

| Analytical Thinker To solve the Corporate Safe Challenge, let's apply the given logical rules step by step to deduce the correct sequence of code entries: 1. List all Executives CEO, CFO, CTO, COO, CMO 2. Apply Rule 1: CEO's Position The CEO's code must be entered either first or last. This means we have two scenarios to explore: CEO first or CEO last. 3. Apply Rule 3 and 4 Together: CFO, CMO, and COO's Placement Since the CFO's code must come immediately before the CMO's, and the COO's code must be entered before the CMO's (but not immediately), it suggests a sequence where CFO and CMO are towards the end, but we also need to account for the COO being before CMO. This could initially suggest a sequence like COO, CFO, CMO if not considering the CEO's position or the CTO's restrictions. 4. Apply Rule 2: CTO's Placement Restrictions The CTO cannot follow the CFO directly or be placed directly before the COO. This rule significantly limits where the CTO can be placed, especially considering the CFO-CMO placement rule. Determining the Sequence Scenario 1: CEO First If the CEO is first, the last positions must accommodate the CFO-CMO sequence, considering the COO must be before CMO but not necessarily directly. The CTO cannot be directly after CFO or right before COO, further complicating its placement. Given these constraints, placing the CEO first means the sequence could potentially end with CFO-CMO, but the COO and CTO's placement needs careful consideration. Scenario 2: CEO Last If the CEO is last, we need to place the other executives in such a way that all rules are satisfied, with the CEO's placement now fixed at the end. The sequence must have the CFO immediately before the CMO, and the COO somewhere before the CMO. Given the CTO's restrictions, it cannot be placed after CFO (due to Rule 2). Conclusion Let's construct the sequence based on Scenario 2 (CEO Last), as it provides a clearer path to satisfying all rules: CTO Placement : Considering the CEO is last, and to satisfy the CTO's restrictions (Rule 2), the CTO cannot be directly before the COO (with the COO and CMO sequence needing to be uninterrupted by the CTO) and not directly after the CFO, placing the CTO first seems the most logical step. COO Placement : The COO must be before the CMO but is not restricted to being directly before the CMO, allowing for flexibility in placement. However, with the CEO last and the CTO likely placed first to avoid conflict with the CFO and COO, the COO can fit before the CFO-CMO sequence but after the CTO. CFO-CMO Sequence : This pair is locked in sequence due to Rule 3, and with the CEO at the end, they would naturally fit towards the end but before the CEO. CEO Last : Confirmed by the choice of scenario. Thus, the sequence that fits all criteria is: First : CTO Second : COO (Rule 4 requires COO before CMO, and placing it here satisfies all conditions without breaking Rule 2's restrictions on the CTO) Third : CFO (immediately before CMO as per Rule 3) Fourth : CMO (immediately after CFO) Fifth : CEO (as per Scenario 2, fulfilling Rule 1) Final Sequence: CTO, COO, CFO, CMO, CEO This sequence satisfies all the given logical rules: The CEO is last. The CTO's placement avoids being directly after the CFO and directly before the COO. The CFO is immediately before the CMO. The COO is placed before the CMO, not necessarily immediately. Each executive's code is entered once, fulfilling the uniqueness criterion. |
|---|

Simply by creating a GPT that specialises in classical methods of analytical thinking, we are able to add value and get a better response than we do when using native ChatGPT 4.

Opening the safe, by ChatGPT

---

# Chapter 12. Solving Causal Problems with CoT Prompting

A common problem-solving method that relates to scenarios in which "one thing follows another" is Business Process Analysis.

Classically, Business Process Analysis is used in businesses or manufacturing environments to determine the optimum chain of discrete activities which will result in the creation of the desired service or manufactured item. We can however, repurpose Business Process Analysis for our needs and use it as a problem solving methodology for general cause-and-effect problems.

This chapter provides a high level introduction to business processes in general and Business Process Analysis in particular.

## Introduction to Business Processes

A business process is a structured set of activities or tasks, organised to produce a specific service or product within an organisation. Business processes guide organisations to producing consistent and reliable results; the foundation of all successful corporations is well-defined business processes.

When business processes are well defined:

- Staff know what they are meant to be doing.

- Quality goods and services are provided in a predictable manner.

- Each step in the business process can be measured, optimised and have rough edges smoothed out.

- The work flowing through each step of a business process can be measured, controlled and optimally routed.

| The term "Business Process" often refers to a set of interrelated activities in an office or a services company. However, this term can also be applied in a manufacturing context, where it refers to the methods involved in producing goods and services. This could include the steps in a factory assembly line, the steps in quality control mechanisms, or the steps in supply chain management. |
|---|

## Basic Ideas of a Business Process

The most fundamental idea of a business process is the decomposition of a required activity into sequential and discrete steps. This simplifies complex tasks and ensures that each step effectively contributes towards the ultimate goal.

For example, we could just consider welding a car door in a car factory as one step that is performed by the factory, or we could split it up into multiple discrete steps, as follows:

| Automated Welding Process Business Process i. Programming the Welding Robots : Before welding starts, robots are programmed with precise welding paths. This includes the welding speed, angle, and duration for each weld. ii. Positioning the Door Panel : The door panel is positioned accurately within the welding station. Clamps and sensors are used to ensure the panel is held in place correctly during the welding process. iii. Welding Execution : The robots execute the welding process, joining the smaller parts to the door panel. Each weld is monitored for quality, such as depth and strength. iv. Cooling : Post-welding, the door undergoes a cooling period. After cooling, each weld is inspected for defects like cracks or weak joints. v. Finishing Touches : After welding, any excess material (like welding splatter) is cleaned off, and the weld areas are polished or ground down if necessary. vi. Final Inspection : The welds are inspected with a combination of visual checks and testing methods like ultrasonic testing, to ensure quality. |
|---|

The advantage of splitting up the welding into discrete steps is that we can then concentrate on the efficiency, quality and throughput of each step separately, as well as optimising the way that work-in-progress parts flow from one step to the next.

## Actions, Inputs and Outputs

For a business process to function effectively, every step must be clearly defined in terms of its inputs, outputs, and actions.

- Actions are the tasks or activities performed in the step. They represent the transformation that takes place in the step, where inputs are converted into outputs.

In the welding step, the "action" is the actual welding performed by robots.

- Inputs are the precursors of a process step; they can be any or all of the following:

➢Materials: Raw materials or components needed for the process.

➢Information: Data, instructions, or guidelines necessary to carry out the step.

➢Resources: Tools, equipment, and human resources essential for the task.

The quality and availability of inputs directly impact the effectiveness of the process. For instance, in a welding process, the quality of the welding robots determines the quality of the weld that they will produce.

- Outputs are the products or results of the process step. They can be:

➢Physical Products: Like a welded car door.

➢Services: In service industries, outputs could be the delivery of a service. For example, the output of a mail delivery service is that a letter has been delivered to the recipient.

➢Information: Reports, updates, or feedback for the next steps.

Outputs must meet predefined quality standards and be ready for the next stage of the process or for delivery to the customer.

By thoroughly structuring each step in the process, Business Process Analysis allows us to identify areas for improvement, manage resources more effectively, and ensure that each step contributes optimally towards the final goal of producing a high-quality product.

Welding Robot. Wikimedia Commons

---

# Chapter 13. CoT Prompting using Business Process Analysis

## Casting Causal Problems as a Business Process

In Chapter 8. Framing Problems, we talked about the idea of framing (or "casting") a real-world problem as a specific problem type. We can cast any problem that involves a sequence of problem-solving steps in terms of a business process.

In other words, we can get an AI to think of a general problem as a "pseudo-business process" and solve it using business process analysis.

Doing this forces the AI to break down the initial problem into a series of steps that have to be solved each on its own merits, and then join the steps together, to reach the correct answer.

## The Hugging Face GAIA Dataset

The Hugging Face GAIA (general AI assistant) Dataset (https://huggingface.co/datasets/gaia-benchmark/GAIA) is a AI benchmark designed to evaluate the abilities of next-generation Language Models (LLMs).

The GAIA dataset includes challenges with three levels of difficulty:

- Level 1 : Questions that generally require no extra tools besides the AI reasoning engine itself; or at most one tool but no more than 5 steps.

- Level 2 : Questions that generally involve more steps, roughly between 5 and 10, and combine the need to use different extra tools in addition to the actual AI reasoning engine.

- Level 3 : Questions for a near perfect general AI assistant. These questions require the ability to take arbitrarily long sequences of actions, use any number of tools, and access worldwide information in general.

Let's see if we can lift ChatGPT 4's ability to meet the Hugging Face GAIA challenge.

## Finding Nemo

For example, let's take an AI-thinking challenge from the Hugging Face General AI Assistant dataset (https://huggingface.co/datasets/gaia-benchmark/GAIA?row=1).

| I’m researching species that became invasive after people who kept them as pets released them. There’s a certain species of fish that was popularised as a pet by being the main character of the movie Finding Nemo. According to the USGS, where was this fish found as a non-native species, before the year 2020? I need the answer formatted as the five-digit zip codes of the places the species was found, separated by commas if there is more than one place. |
|---|

Let's see what happens if we pose this question directly to ChatGPT 4.

| User Solve : I’m researching species that became invasive after people who kept them as pets released them. There’s a certain species of fish that was popularised as a pet by being the main character of the movie Finding Nemo. According to the USGS, where was this fish found as a non-native species, before the year 2020? I need the answer formatted as the five-digit zip codes of the places the species was found, separated by commas if there is more than one place. ChatGPT Error analysing I attempted to retrieve the ZIP codes for the locations where the clownfish (popularised by the movie "Finding Nemo") was found as a non-native species according to the USGS. However, due to the constraints of my environment, I'm unable to directly access the internet or external databases, including the USGS database. To find the specific ZIP codes where the clownfish was found as a non-native species, you can manually search the USGS database for records of clownfish sightings or reports. Once you have the locations, you can then use an online tool or map service to convert these location names into their corresponding five-digit ZIP codes. If you can provide me with the specific locations from the USGS database, I can then assist you in finding the corresponding ZIP codes. |
|---|

ChatGPT fails to find the answer and claims that the required data is unavailable.

Now let's use a GPT called Process Designer (https://t.ly/9rJVk) to break down the original problem into discrete steps, framed as a business process.

| You Break up this problem into multiple steps in a business process, for each step specify input, processing and output: I’m researching species that became invasive after people who kept them as pets released them. There’s a certain species of fish that was popularised as a pet by being the main character of the movie Finding Nemo. According to the USGS, where was this fish found as a non-native species, before the year 2020? I need the answer formatted as the five-digit zip codes of the places the species was found, separated by commas if there is more than one place. Process Designer I understand, let's break down your original problem into a detailed business process with specific references to your query: Business Process : Tracking Invasive Species Spread Due to Pet Release 1. Problem Identification Input : The need to research a specific species that became invasive due to pet release. Processing : Identifying the species as the one popularised by the movie "Finding Nemo." Output : A clear research goal focused on tracking the non-native spread of this particular fish species. 2. Data Sourcing Input : The specified fish species from "Finding Nemo." Processing : Determining USGS as the authoritative source for geographical data on the species. Output : Selection of USGS as the primary data source for this research. 3. Data Collection Input : USGS as the selected data source. Processing : Collecting data from USGS regarding the non-native occurrences of the specified fish species. Ensure the data timeframe is limited to before 2020. Output : A dataset from USGS detailing where the species was found as a non-native species before 2020. 4. Data Analysis Input : USGS dataset on the non-native occurrences of the species. Processing : Extracting specific instances and locations of non-native occurrences from the dataset. Output : A list of locations (potentially in various geographical formats) where the species was found. 5. Data Formatting Input : List of locations where the species was found. Processing : Converting the locations into their corresponding five-digit zip codes. If a location does not directly correspond to a zip code, additional geographical cross-referencing might be required. Output : A formatted list of five-digit zip codes, separated by commas if multiple locations are identified. 6. Verification and Validation Input : Formatted list of zip codes. Processing : Cross-checking the accuracy of the zip codes against the original data and geographical standards. Output : A verified and validated list of zip codes where the species was found. 7. Documentation and Reporting Input : Verified list of zip codes and research data. Processing : Compiling the findings into a formal report with methodology, sources, and observations. Output : A comprehensive report detailing the non-native zip codes of the species' occurrence. |
|---|

Now let's go back to ChatGPT 4 and ask it to solve the original problem using the business process defined by the Process Designer GPT:

| User Solve this problem: "I’m researching species that became invasive after people who kept them as pets released them…" using this method "Business Process: Tracking Invasive Species Spread Due to Pet Release 1. Problem Identification Input…" ChatGPT The species of fish popularised by the movie "Finding Nemo" is the clown anemonefish, scientifically known as Amphiprion ocellaris . This species, noted for its striking orange coloration with three white bars, is native to the Indo-Pacific Ocean, typically found in tropical marine habitats associated with rocky or coral reefs . Regarding its non-native occurrences in the United States, the USGS Nonindigenous Aquatic Species Database provides specific information. This database monitors, records, and analyses sightings of nonindigenous aquatic plant and animal species throughout the United States. It's a comprehensive source for tracking the spread of non-native species, including the clown anemonefish. According to the USGS data, there was a recorded instance of Amphiprion ocellaris in the United States prior to 2020. This occurrence was in Florida, specifically in Pinellas County. The fish was collected in July 2018 at Fred Howard Park. The USGS database categorises this introduction as likely due to an aquarium release. Following its discovery, the specimen was removed alive and transferred to the Clearwater Marine Aquarium. For the purpose of your research which requires zip codes, the relevant zip code for Fred Howard Park, Pinellas County, Florida, where the clown anemonefish was found, is 34689. It's important to note that the USGS database is a dynamic tool, regularly updated with new data to ensure accuracy and relevance. It includes not only occurrences but also interactive maps, species profiles, and detailed information about each species' introduction and impact on local ecosystems. This information underscores the importance of responsible pet ownership and the potential ecological impacts of releasing non-native species into local environments. The spread of such species can have unforeseen and often detrimental effects on native biodiversity and ecosystems. For further details and research, you can explore the USGS Nonindigenous Aquatic Species Database directly here . |
|---|

This time, ChatGPT's answer of 34689, is exactly correct.

---

By decomposing the original problem statement into a discrete sequence of steps that the AI must solve to reach the answer (i.e. by creating a pseudo-business process) we allow ChatGPT to think the problem through step-by-step and to reach the correct answer.

This effectively demonstrates that by using CoT Prompting we can "amplify" the power of a generative AI such as ChatGPT 4, and allow it to solve problems that appear out of its reach initially.

## Finding a University

The next AI-thinking challenge is also taken from the Hugging Face General AI dataset (gaia-benchmark/GAIA - Datasets at Hugging Face).

| All of the individuals who formally held the position of United States secretary of homeland security prior to April 2019, excluding those who held the position in an acting capacity, have a bachelor's degree. Of the universities that these bachelor's degrees were from, which is the westernmost university and which is the easternmost university? Give them to me as a comma-separated list, I only want the name of the cities where the universities are located, with the westernmost city listed first . |
|---|

Let's see what ChatGPT 4 makes of this problem, unaided:

| User All of the individuals who formally held the position of United States secretary of homeland security prior to April 2019, excluding those who held the position in an acting capacity, have a bachelor's degree. Of the universities that these bachelor's degrees were from, which is the westernmost university and which is the easternmost university? Give them to me as a comma-separated list, I only want the name of the cities where the universities are located, with the westernmost city listed first. ChatGPT Error analysing I encountered a technical limitation in obtaining the geographical longitudes of the cities directly. However, we can determine the westernmost and easternmost universities based on their known geographic locations in the United States. Santa Clara University is located in Santa Clara, California, which is on the West Coast of the United States. Harvard University and Morehouse College are located in Cambridge, Massachusetts, and Atlanta, Georgia, respectively. Of these, Cambridge is further east. Therefore, the westernmost university among these is Santa Clara University in Santa Clara, California, and the easternmost is Harvard University in Cambridge, Massachusetts. The comma-separated list, with the westernmost city listed first, is: "Santa Clara, California, Cambridge, Massachusetts". |
|---|

Santa Clara is right, but Cambridge is wrong. Now let's convert the problem into business process format, using the Process Designer GPT.

| You Break up this problem into multiple steps in a business process, for each step specify input, processing and output: All of the individuals who formally held the position of United States secretary of homeland security prior to April 2019, excluding those who held the position in an acting capacity, have a bachelor's degree. Of the universities that these bachelor's degrees were from, which is the westernmost university and which is the easternmost university? Give them to me as a comma-separated list, I only want the name of the cities where the universities are located, with the westernmost city listed first . Process Designer Step 1 : Identification of Former Secretaries of Homeland Security Input : List of individuals who held the position of United States Secretary of Homeland Security prior to April 2019, excluding acting secretaries. Processing : Research and compilation of names. Output : A verified list of former Secretaries of Homeland Security. Step 2 : Collection of Educational Backgrounds Input : The list of former Secretaries of Homeland Security. Processing : Gathering information about the bachelor's degrees of these individuals, including the universities they attended. Output : A list of universities where these secretaries obtained their bachelor's degrees. Step 3 : Geographical Analysis of Universities Input : List of universities from Step 2. Processing : Determine the geographical location (longitude and latitude) of each university. Output : Geographical coordinates of each university. Step 4 : Determining Westernmost and Easternmost Universities Input : Geographical coordinates of universities from Step 3. Processing : Analysing the coordinates to identify the westernmost and easternmost universities. Output : Names of the westernmost and easternmost universities. Step 5 : Extraction of City Names Input : Names of the westernmost and easternmost universities (from Step 4). Processing : Research to identify the cities where these universities are located. Output : Names of the cities where the westernmost and easternmost universities are located. Step 6 : Formatting Final Output Input : Names of the cities from Step 5. Processing : Arranging the city names in the desired format, with the westernmost city listed first. Output : Comma-separated list of the cities, in the specified order. |
|---|

And now let's go back to ChatGPT and ask it to solve the original problem using the problem-solving method expressed in terms of a business process.

| User Solve this problem "All of the individuals who formally held the position of United States secretary of homeland security prior to April 2019, excluding those who held the position in an acting capacity, have a bachelor's degree…" using the following method "Step 1: Identification of Former Secretaries of Homeland Security Input:.." Show inputs and outputs for each step discreetly. ChatGPT To address your problem, here's the step-by-step process: Step 1 : Identification of Former Secretaries of Homeland Security Input: List of individuals who held the position of United States Secretary of Homeland Security prior to April 2019, excluding acting secretaries. Output: The verified list includes Tom Ridge, Michael Chertoff, Janet Napolitano, Jeh Johnson, John F. Kelly, and Kirstjen Nielse n ​ ​ . Step 2 : Collection of Educational Background s Tom Ridge: Bachelor of Arts from Harvard University, Cambridge, Massachusett s ​ ​ . Further Research Required: For the educational backgrounds of Michael Chertoff, Janet Napolitano, Jeh Johnson, John F. Kelly, and Kirstjen Nielsen. Step 3 : Geographical Analysis of Universities Input: List of universities from Step 2. Output: Still pending due to incomplete data from Step 2. Step 4 : Determining Westernmost and Easternmost Universities Input: Geographical coordinates of universities from Step 3. Output: Still pending due to incomplete data from previous steps. Step 5 : Extraction of City Names Input: Names of the westernmost and easternmost universities (from Step 4). Output: Still pending due to incomplete data from previous steps. Step 6 : Formatting Final Output Input: Names of the cities from Step 5. Output: Still pending due to incomplete data from previous steps. Next Steps: Continue research to collect educational backgrounds of the remaining former Secretaries of Homeland Security. Once this information is complete, the subsequent steps can be carried out to identify the westernmost and easternmost universities, and finally, the cities of these universities. You Research: Step 2: Collection of Educational Backgrounds Tom Ridge: Bachelor of Arts from Harvard University, Cambridge, Massachusett s ​ ​ . Further Research Required: For the educational backgrounds of Michael Chertoff, Janet Napolitano, Jeh Johnson, John F. Kelly, and Kirstjen Nielsen. ChatGPT Here is the completed educational background of each former United States Secretary of Homeland Security prior to April 2019, excluding acting secretaries: Tom Ridge: Bachelor of Arts from Harvard University, Cambridge, Massachusett s ​ ​ . Michael Chertoff: Bachelor of Arts from Harvard College, Cambridge, Massachusetts, and Juris Doctor from Harvard Law Schoo l ​ ​ . Janet Napolitano: Bachelor of Science summa cum laude in political science from Santa Clara University, and Juris Doctor from the University of Virgini a ​ ​ . Jeh Johnson: Bachelor of Arts from Morehouse College and Juris Doctor from Columbia Universit y ​ ​ . John F. Kelly: Bachelor’s degree from the University of Massachusetts Boston and a Master of Arts degree in National Security Affairs from the Georgetown School of Foreign Servic e ​ ​ . Kirstjen Nielsen: Bachelor of Science degree from the Georgetown School of Foreign Service and Juris Doctor from the University of Virginia School of La w ​ ​ . With this information, we can now proceed to Step 3 of the process: the geographical analysis of the universities attended by these former Secretaries. You Proceed. ChatGPT Step 3: Geographical Analysis of Universities Based on the educational backgrounds of the former United States Secretaries of Homeland Security, here are the universities they attended: Tom Ridge: Harvard University, Cambridge, Massachusetts . Michael Chertoff: Harvard College and Harvard Law School, Cambridge, Massachusetts. Janet Napolitano: Santa Clara University, Santa Clara, California, and the University of Virginia, Charlottesville, Virginia. Jeh Johnson: Morehouse College, Atlanta, Georgia, and Columbia University, New York City, New York. John F. Kelly: University of Massachusetts Boston, Boston, Massachusetts, and Georgetown School of Foreign Service, Washington D.C. Kirstjen Nielsen: Georgetown School of Foreign Service, Washington D.C., and the University of Virginia School of Law, Charlottesville, Virginia. Now, let's determine the geographical locations (longitude and latitude) of each university: Harvard University: Cambridge, Massachusetts. Santa Clara University: Santa Clara, California. University of Virginia: Charlottesville, Virginia. Morehouse College: Atlanta, Georgia. Columbia University: New York City, New York. University of Massachusetts Boston : Boston, Massachusetts. Georgetown School of Foreign Service : Washington D.C. I will calculate the longitude and latitude coordinates for these universities to determine the westernmost and easternmost universities. Error analysing It seems that there was an issue with fetching the geographical coordinates for the universities. As an alternative approach, I can provide the longitudinal coordinates of these locations based on known geographical data, which should allow us to identify the westernmost and easternmost universities. Let's proceed with that approach. ​​ Based on the longitudinal coordinates, the westernmost university among those attended by the former United States Secretaries of Homeland Security (excluding acting secretaries) prior to April 2019 is Santa Clara University in Santa Clara, California. The easternmost university is the University of Massachusetts Boston in Boston, Massachusetts. Proceeding to the next steps: Step 4 : Determining Westernmost and Easternmost Universities Input: Geographical coordinates of universities. Output: Westernmost - Santa Clara University, Easternmost - University of Massachusetts Boston. Step 5 : Extraction of City Names Input: Names of the westernmost and easternmost universities. Output: Santa Clara, California (westernmost) and Boston, Massachusetts (easternmost). Step 6 : Formatting Final Output Input: Names of the cities from Step 5. Output: Santa Clara, California, Boston, Massachusetts. Therefore, the final formatted output in a comma-separated list, with the westernmost city listed first, is: "Santa Clara, California, Boston, Massachusetts" . |
|---|

A bit rocky, but the discrete problem-solving steps allowed seeing where problems were encountered and continuing the conversation with ChatGPT, which resulted in a more satisfactory user experience as well as the correct answer, Santa Clara and Boston.

---

## Conclusion

Using CoT Prompting to expand real-world causal problems into business process format allows generative AI to:

- Concentrate on one task at a time.

- Show its working for each step, which allows the user to see if and where the AI bot has gone wrong.

- Have a conversation with the user about steps it is stuck on, or not sure about.

This increases the AI's ability to solve complex "cause and effect" type problems and provides a rich, transparent and interactive user experience.

Success!, by ChatGPT

---

# Chapter 14. Introduction to Systems Thinking

This and the following chapters explain what systems analysis is, and how it is used to solve problems that require looking at the whole picture.

## The Definition of a System

In everyday conversation we often talk about systems:

- The system wasn't fair to him.
- The computer system isn't working.
- The concert had an incredible sound system.

But just what is a system?

| Definition of a System A system is a complex entity made up of interrelated and interdependent components that work together to achieve a specific purpose. It is a self-contained unit, internally consistent and capable of functioning autonomously. Systems can be either natural or man-made, ranging from living beings to machines and societal structures. |
|---|

In the above examples, the word "system" carries the following meanings:

- Audio Systems : The statement "the concert had an incredible sound system" refers to an audio technology setup. In this context, the sound system is an assembly of electronic devices that work together to capture, amplify, and reproduce sound. This can include microphones, mixers, amplifiers, and speakers.

Each component has a distinct function, and all the components work together to produce a high-quality sound suitable for the concert style, audience and concert location.

- Information Systems : The phrase "the computer system isn't working" refers to a technological setup. Here, a system is a group of interrelated hardware computer components and software that work together, which could be on an individual computer or a network of devices.
- Societal structures : When people say, "The system wasn't fair to him," they are referring to societal, legal, or organisational structures. In this context, a system implies a set of rules, and procedures that govern how people are treated or how decisions are made. "The system wasn't fair to him" means the societal rules are structured in a way that led to an unfair outcome for the individual concerned.

In all these cases, a "system" is defined as a complex set of parts or rules that are interconnected and function together, providing physical, informational or behavioural outcomes.

## Examples of Systems

Some more examples of systems include:

Cars

System Type: Man-made mechanical system.

Components: Engine (power generation), wheels (mobility), chassis (structural integrity), transmission (power distribution), and fuel system (energy supply).

Function: Cars provide transportation, enabling efficient movement of people and goods over distances.

Factories

System Type: Man-made industrial system.

Components: Production lines (manufacturing process), machinery (production tools), raw materials (input for production), finished products (output), storage units (product preservation) and workers (labour force).

Function: Factories convert raw materials into finished goods, playing a pivotal role in economies and consumer supply chains.

Economies

System Type: Man-made societal system.

Components: Individuals (consumers, labour force), businesses (production, services), banks (financial services, capital), and government institutions (regulation, policymaking).

Function: Economies manage the production, distribution, and consumption of goods and services, and control wealth and resource allocation.

Rivers

System Type: Natural ecological and hydrological system.

Components: Riverbed (physical pathway), source (e.g. spring or glacier), tributaries (contributory streams), aquatic life (biodiversity) and mouth (confluence with another body of water, e.g. the sea).

Function: River systems support plant growth and animal life, facilitate water transport, and contribute to geographical processes.

In all these examples, the "system" consists of interconnected elements working synergistically to maintain internal stasis (an internally balanced state), perform specific functions and achieve overall system objectives.

[Imagen: river rhine black and white free photo]

The Rhine River. Creator: domeckopol

---

# Chapter 15. Systems Analysis

Systems analysis is an intricate process that can be broken down into the following steps.

## Understanding the System as a Whole

The first step in systems analysis is getting a high level view of the system as a whole. This involves the following steps.

### Defining the System

Defining the system focuses on delineating what is included within the system (internal components and processes) and what is considered outside of it (external factors and entities).

For example:

| System | Inside the System | External to the System |
|---|---|---|
| Information Technology (IT) System | Hardware (servers, routers, workstations), software applications (databases, user interfaces, middleware), data, and the IT team. | External internet service providers, users accessing the system from outside the organisation, third-party software and hardware vendors, and regulatory bodies. |
| Environmental Ecosystem | Living organisms (plants, animals, microbes), physical components (soil, water, air), and the interactions between them. | Adjacent ecosystems, human interventions ( pollution, deforestation), and climate changes beyond the local environment. |
| Manufacturing Process System | Machinery, workers, raw materials, production protocols, and internal logistics. | Suppliers of raw materials, distribution partners, market demand, and regulatory standards. |
| Education System | Students, teachers, curriculum, educational materials (books, online resources), and school infrastructure (classrooms, laboratories). | Parents, educational policy makers, external examination bodies, and after-school education providers. |

In each example, defining the system involves clearly identifying which components, processes, and interactions are integral to the system, and which factors influence the system from the outside.

School, by ChatGPT

---

### System Behaviour

This part of systems analysis involves understanding the effect that the system has on its environment, and the way in which it reacts to its environment.

Relevant factors here are:

- Inputs : These are the resources that the system consumes from its environment. This can encompass a wide range of things, from physical materials and energy to information and financial resources.
- Outputs and Impact : A system may "behave" by intentionally producing a certain type of output or by unintentionally impacting its environment.

For example, a factory's intended output is the products it produces, but it may also have environmental impacts through waste production or energy consumption.

- Adaptation : Systems often need to adapt to changes in their external environment to maintain functionality or to take advantages of new opportunities.

For instance, an ecosystem might adapt to changes in climate conditions through changed migration patterns, or a business may change its product lines due to changes in market conditions.

- Interaction with Other Systems: The behaviour of a system also includes its interactions with other systems in its environment.

These interactions can be cooperative, in which case the introduction of new systems strengthens the existing system, or competitive, in which case the introduction of new systems weakens the existing system.

---

## Understanding Component Elements

The process of systems analysis continues with identifying the component elements of the system, and the nature of each element.

### Component Identification

The initial phase entails identifying the elements that constitute the system. These may range from tangible, physical components like machinery in a manufacturing setup to intangible, abstract elements such as data in an information system.

### Classification of Component Elements

After identification, components can be classified into three primary categories based on their roles and characteristics:

- Static Structural Components : These elements serve as the backbone of the system, providing essential support and structure. While they do not participate directly in the system's operations, their presence is critical for maintaining the system's stability and integrity.
- Dynamic Functional Components : These components are directly involved in executing the system's primary functions. They perform processes and actions that progress the system toward its objectives.
- Reactive Components : These components play a passive role, responding to the activities of dynamic elements.

### Analysing Component Behaviour and Functionality

The terms "behaviour" and "functionality" are often used systems analysis, they mean slightly different things:

- Functionality refers to the functions that a component is designed to perform. It describes what the component can do, the tasks it can accomplish, or the services it provides.

- Behaviour refers to how a component, system, or process responds or operates under various conditions or stimuli. Behaviour can include dynamic responses to input, changes over time, and adaptations to external factors.

Understanding component functionality and behaviour is required to understand which elements cause specific internal system behaviours and provide different system functionalities.

## Component Interaction

The essence of systems analysis lies in the interactions between the various elements that make up the system. Component interaction analysis includes:

- Integration : Looking at how components are brought together to work as a unified whole.
- Communication : Analysing how components communicate and exchange information or resources.
- Dependencies : This involves identifying how the functioning of one component might rely on the output or proper functioning of another.

Understanding component interactions provides an understanding of how the component elements coalesce to create and energise the holistic system.

## System Layout

The system layout details the arrangement of component elements, both spatially and logically. This arrangement determines how individual components are positioned and interact with each other.

Key aspects of system layout analysis include:

- Spatial Arrangement : This refers to the physical placement of components relative to each other and the system boundaries.
- Logical Configuration : This deals with the abstract organisation of components, such as software modules or data flow paths.

## Operational Rules

Operational rules define the permissible actions, interactions, and states within the system, serving as the guidelines for orderly system conduct and decision-making.

Elements of operational governance include:

- Permissible Actions : This defines what actions are allowed within the system.
- Interaction Protocols : This outlines the agreed method via which components interact.
- State Regulations : This specifies the allowable states within the system.

By adhering to the system operational rules the system is able to gain operational efficiencies over a wide range of external conditions and internal states.

## System Constraints and Feedback Loops

### System Constraints

System constraints refer to the limitations or restrictions within which a system operates. These constraints can be external, originating from the environment in which the system operates, or internal, arising from the system's inherent design and components.

Types of System Constraints

- Resource Constraints : Limitations due to the availability of resources like materials, energy, or information.
- Design Constraints : Inherent limitations due to the system's architecture, such as capacity limits, efficiency, or scalability.
- Environmental Constraints : External factors such as regulatory policies, market conditions, or ecological impacts that affect system operations.
- Operational Constraints : Restrictions related to how a system is used or maintained, including user skill levels or maintenance practices.

For example, imagine a child building a sandcastle on the beach. The "system" in this scenario is the process of building the sandcastle. The following constraints limit or influence how the child can build their sandcastle.

| A process, such as building a sandcastle, can also be considered as a system. In this case the infrastructure of the system is primarily conceptual; it is the fact that we have decided to set about the task of building a sandcastle. This “decisional infrastructure” (state of affairs) is augmented by the physical components that make the activity possible, such as sand and tools. |
|---|

- Resource Constraints (Internal) : The available tools and amount of sand. If the child only has a small bucket and shovel, their ability to build a large or complex sandcastle is limited.
- Design Constraints (Internal) : The child's artistic talent and skill level in building sandcastles. An idea for a sandcastle with tall towers and intricate walls can't be implemented without considerable skill and knowledge of the sand as a building medium.
- Environmental Constraints (External) : These are factors like the tide coming in, rain, or other beachgoers walking around. If the tide is coming in, the child has limited time to build the sandcastle before it gets washed away.
- Operational Constraints (External/Internal) : This is about how the child uses their tools and sand. If they decide to build close to the water where the sand is wetter, the castle might be more stable. If they decide to build further away from the water, the sand may not hold together as well but they will have longer to build before the sandcastle is washed away by the tide.

In simple terms, system constraints are the various internal and external factors that limit or define what a system can or cannot do; they shape how the system operates and what it can achieve.

### Feedback Loops

Feedback loops are self-correcting or self-enhancing mechanisms through which a system self-regulates and adapts to changes. They are fundamental in maintaining system stability and facilitating dynamic responses to internal and external changes.

Feedback loops occur in all types of systems, such as in biological systems where they maintain the conditions necessary for life, in social systems where they preserve law and order, and in mechanical systems where they ensure safe system functioning.

Types of Feedback Loops

Generally speaking, we can identify two types of feedback loops:

- Positive Feedback Loops : These feedback loops amplify changes or deviations, leading to exponential growth or decline in certain system behaviours. For example, in an economy, increased investment can lead to more jobs, which in turn leads to more spending and further investment.
- Negative Feedback Loops : These feedback loops counteract changes, promoting stability and equilibrium. For instance, in a car's cooling system, a thermostat regulates the engine temperature by adjusting the cooling rate. If the engine's temperature increases then the cooling system works harder to bring the temperature back down.

The correct design of feedback loops is crucial in ensuring that systems grow at a healthy rate, function at a maintainable energy level, and don't self-destruct due to excessive growth or activity.

---

### Combining System Constraints and Feedback Loops

System constraints and feedback loops work together to ensure a system functions effectively and efficiently within its safe operating constraints. Constraints define the boundaries within which a system can operate effectively, while feedback loops provide the mechanism for the system to remain within these boundaries and adapt as necessary.

For example, the RPM (revs per minute) constraint of a car engine defines its operational limits of the engine; the feedback loops provided by control systems maintain the engine's efficiency and performance within this constraint, so ensuring that the engine operates smoothly, effectively and safely.

[Imagen: 1899 Daimler 12 HP - PICRYL - Public Domain Media Search Engine Public  Domain Search]

1899 Daimler, Creator: National Motor Museum in Beaulieu

---

# Chapter 16. CoT Prompting with Systems Analysis

## Using AI in Classical Systems Analysis

AI has many and varied uses in actual Systems Analysis, for example:

- Optimising Manufacturing Processes : By analysing vast amounts of production data, AI can redesign workflows and machinery layouts, leading to significant improvements in productivity and cost reduction.

- Hospital Resource Management : AI can analyse patient admission rates, treatment times, staff schedules, and resource availability to develop a new scheduling system that maximises the use of available beds and medical equipment.

AI has the ability to do more effective number-crunching than human analysts, therefore it has the ability to spot solutions that evade conventional analysis.

## Casting General Problems as Systems Problems

In addition to using AI to solve classical systems problems, we can also augment AI's problem solving abilities by using CoT Prompting to cast general problems as system problems, and then following systems analysis methods to solve this reworded problem.

In other words, reconfiguring a general problem into systems terms can assist the AI in organising its reasoning and reaching an accurate conclusion.

Let's see what happens when we apply AI systems analysis to scenarios which do not, at first sight, seem to have anything to do with systems analysis.

---

## Solving a Logic Puzzle

The following logic puzzle is taken from My Best Mathematical And Logic Puzzles, by Martin Garner  (https://archive.org/stream/my-best-mathematical-and-logic-puzzles).

| THREE HIGH SCHOOLS—Washington, Lincoln and Roosevelt— competed in a track meet. Each school entered one man, and one only, in each event. Susan, a student at Lincoln High, sat in the bleachers to cheer her boyfriend, the school’s shot-put  champion. When Susan returned home later in the day, her father asked how her school had done. “We won the shot-put all right,” she said, “but Washington High won the track meet. They had a final score of 22. We finished with 9. So did Roosevelt High.” “How were the events scored?” her father asked. “I. don’t remember exactly,” Susan replied, “but there was a certain number of points for the winner of each event, a smaller number for second place and a still smaller  number for third place. The numbers were the same for all events.” (By “number” Susan of course meant a positive integer.) “How many events were there altogether?” “Gosh, I don’t know, Dad. All I watched was the shot-put.” “Was there a high jump?” asked Susan’s brother. Susan nodded. “Who won it?” Susan didn’t know. Incredible as it may seem, this last question can be answered with only the information given. Which school won the high jump? |
|---|

First, let's ask ChatGPT to solve this puzzle without any external assistance.

| You Solve this puzzle: THREE HIGH SCHOOLS—Washington, Lincoln and Roosevelt— competed in a track meet. Each school entered one man, and one only, in each event… ChatGPT This puzzle involves deducing the winner of the high jump event based on the information provided. Let's analyse the data: Scoring System : There are three places in each event, each assigned a certain number of points (positive integers) - let's call them A , B , and C for first, second, and third places, respectively, with A > B > C . Overall Scores: Washington High: 22 points Lincoln High: 9 points Roosevelt High: 9 points Known Outcomes: Susan's boyfriend from Lincoln High won the shot-put. To solve this puzzle, we need to find a scoring system that fits these constraints and then determine the winner of the high jump. The key is to realise that the total number of points must be the same for each school. The sum of the scores of all three schools is 22 + 9 + 9 = 40 points. This total must be distributed among the events, with each event contributing A + B + C points. Let's try to find a scoring system that works with these constraints and determine how many events there were. Then, we can figure out the winner of the high jump . We have identified several potential scoring systems where the sum of points for first, second, and third places is a divisor of Washington High's score (22 points). These scoring systems are: (5, 4, 2) (6, 3, 2) (6, 4, 1) ... ... and many more up to (19, 2, 1). However, not all of these scoring systems are valid for our puzzle. We need to find a system where the total points (40) can be divided evenly among the events. This means that the sum of points for first, second, and third place (A + B + C) should be a divisor of 40. Let's filter these scoring systems to find the ones that meet this criterion. Then, we can determine the number of events and figure out who won the high jump. ​​ Interestingly, none of the identified scoring systems where the sum of points for first, second, and third places is a divisor of Washington High's score (22 points) also divide the total points (40) evenly among the events. This suggests that we need to revisit our assumptions and calculations. Given that Washington High won with 22 points and both Lincoln and Roosevelt Highs had 9 points each, the total points allocated were indeed 40. We need a scoring system where: The sum of points for the three places is a divisor of 22. The same sum is also a divisor of 40. Let's re-evaluate the possible scoring systems under these conditions. We'll consider that the number of points for the first place must be greater than the second, which in turn must be greater than the third, and all must be positive integers. ​​ It appears that there is no scoring system that fits both constraints (being a divisor of both 22 and 40) under the assumptions we have made so far. This indicates that our initial approach might need adjustment. Let's reconsider the problem with a different perspective. The key lies in the distribution of points among the three schools and the total of 40 points. Since Washington High won with 22 points and the other two schools tied with 9 points each, it's evident that Washington High won more events than the other two schools. However, the scoring system must still account for the total of 40 points and the tie between Lincoln and Roosevelt Highs. We'll explore different scenarios for the number of events and the distribution of wins among the schools, keeping in mind that Washington High must have the most wins. Let's calculate these scenarios. ​​ We have found several valid scenarios for the distribution of event wins that align with the given scores and constraints. Each scenario includes a possible scoring system (points for 1st, 2nd, and 3rd places) and the number of 1st, 2nd, and 3rd place finishes for each school. For example, one of the scenarios is: Scoring System: (5, 3, 2) Washington High: 2 first places, 4 second places, 0 third places Lincoln High: 1 first place, 0 second places, 2 third places Roosevelt High: 1 first place, 0 second places, 2 third places Now, we need to determine which school won the high jump. Since Susan's boyfriend from Lincoln High won the shot-put, we know Lincoln High had at least one first-place finish. To identify the high jump winner, we need to find a scenario where only one school other than Lincoln could have won a first place, ensuring that this school must have won the high jump . Let's filter these scenarios to find one where Lincoln High has exactly one first-place finish, and then we can deduce the high jump winner. ​​ (Stopped analysing) |
|---|

Unaided, ChatGPT eventually gave up and did not come to a conclusion.

Now let's use CoT Prompting to solve the puzzle in two phases.

First let's restructure the puzzle into a systems format using a GPT called Systems Question Rephraser (https://t.ly/ax3tz) which is designed for this purpose.

| You Rephrase: Solve this puzzle: THREE HIGH SCHOOLS—Washington, Lincoln and Roosevelt— competed in a track meet. Each school entered one man, and one only, in each event… Systems Question Rephraser System Context : This scenario is set within the framework of a high school track meet system involving three schools - Washington, Lincoln, and Roosevelt. The system's objective is to allocate points based on event performances and determine the overall winner based on the cumulative points. System Components : Active Elements : Competing students from Washington, Lincoln, and Roosevelt High Schools. Passive Elements : Track meet events (including shot-put and high jump), scoring mechanism. Inputs : Performance of students in each event. Outputs : Points awarded per event, total points for each school. System Behaviour : Points are awarded based on event placement: a set number for first place, a lesser number for second, and an even smaller number for third. The total points for each school are aggregated from individual event scores. Feedback Loops : The feedback involves assessing the performance of students in each event and adjusting the total points accordingly. System Constraints : Each school enters one student per event. Points awarded are positive integers and consistent across all events. System Requirements : Initial State : Start of the track meet with zero points for each school. Intermediary States : Allocation of points to schools based on event outcomes. Final State : Final score tally with Washington High winning at 22 points, Lincoln and Roosevelt each with 9 points. Business Rules : The point distribution system for event placements must be consistent across all events. The total score for each school is the sum of points from all events. The winner of the track meet is determined by the highest total score. Rephrased Requirement : Construct a model to analyse the point distribution and event outcomes of a high school track meet system, where each of three schools competes in various events. The model should deduce the winner of the high jump event using the given final scores, event scoring structure, and known outcomes from specific events, while adhering to the constraint that point values are positive integers and consistent across events. |
|---|

The GPT has identified the system elements of active elements, passive elements, system behaviours and "business rules", as well as inputs, outputs and the required initial, intermediary and final system states.

Now let's ask ChatGPT to solve this systems representation of the logic puzzle.

| You Solve this puzzle: "THREE HIGH SCHOOLS—Washington, Lincoln and Roosevelt— competed in a track meet… " Using this methodology: "System Context: This scenario is set within the framework of a high school track meet system involving three schools - Washington, Lincoln, and Roosevelt…" ChatGPT To solve this puzzle, we need to analyse the information given and deduce the winner of the high jump event based on the final scores, event scoring structure, and the known outcome of the shot-put event. Given Information : Schools Involved: Washington, Lincoln, and Roosevelt. Final Scores: Washington - 22 points, Lincoln - 9 points, Roosevelt - 9 points. Event Scoring Structure: A certain number of points for first, second, and third place, the same across all events, with each position getting a lesser amount than the one above it. Shot-Put Event : Lincoln won. Assumptions : There are only three places in each event: first, second, and third. Points are positive integers. At least two events were held: shot-put and high jump. Analysis : Let's denote the points for first, second, and third places as X , Y , and Z respectively. We know that X > Y > Z , and all are positive integers. Since Lincoln won the shot-put, they received X points in this event. Given Lincoln's total is 9 points, it means X =9, as they could not have scored in any other event (otherwise their total would be more than 9). Therefore, for Washington to achieve 22 points and Roosevelt to achieve 9 points, we need to find a combination of Y and Z that satisfies these conditions. Deduction : For Roosevelt: They must have come either second or third in the shot-put (as Lincoln came first). Since they have 9 points, the same as Lincoln, they must have also scored X =9 in another event, meaning they won another event. For Washington: With 22 points and knowing that X =9, they must have won at least one event (9 points) and scored in other events to make up the remaining 13 points. This means they could not have scored just Y and Z points in two events (as the highest they could reach would be 9+ Y + Z which would be less than 22 if Y and Z are positive integers less than 9). Conclusion : Washington must have won at least two events, including the high jump (since Roosevelt won one event, and Lincoln won the shot-put). Thus, Washington High School won the high jump event . |
|---|

Given the rephrased systems representation of the logic puzzle, ChatGPT came immediately and directly to the correct answer.

By rephrasing the logic puzzle as a systems problem, we were able to use CoT Prompting to guide ChatGPT in a direct and efficient path to coming to the correct conclusion.

Now let's use this approach to solve a real-world business problem.

## Solving a Business Problem

The following business problem represents a real-world scenario with which a marketing manager could be presented.

| Optimising International Product Launch Strategy with Quantitative Data Scenario : You are the global marketing director of a multinational company. Your task is to launch two new products, Product X and Product Y, in various international markets. The marketing budget for the next quarter is $200,000. Product X : Profit Margin : $70 per unit Conversion Rate of Ads : 3% in established markets, 1% in new markets Average Cost Per Ad Click : $1.50 in established markets, $2 in new markets Market Sensitivity : Requires an additional 20% budget for customising marketing campaigns in culturally diverse regions Regulatory Costs : Extra $10,000 in markets with strict regulations Product Y : Profit Margin : $120 per unit Conversion Rate of Ads: 1.5% Average Cost Per Ad Click: $2.50 Supply Constraint Impact : Since the raw materials used to make Product Y are also used to make other products, and are in short supply, the manufacturing department has advised that they can only meet 60% of the product demand in the initial phase Complementary Goods Influence : 20% demand boost when paired with specific local products Market Characteristics : Emerging Markets: Growth potential: 25% Risk factor: 15% higher marketing costs due to instability Established Markets: Growth potential: 10% Highly competitive : Requires 30% more budget for effective market penetration. Cultural Diversity : Customization costs increase marketing expenses by 20% in culturally diverse markets Additional Considerations : Global Economic Trends : Currency fluctuation: ±5% change in budget value expected. Competitor Activities : Expected to reduce market share by up to 10% in key markets. Sustainability and CSR : Allocating 5% of the budget to these initiatives could increase brand value and customer loyalty by 15% Problem Statement : Develop an international marketing strategy to allocate the $200,000 budget effectively across different markets for Product X and Product Y. The strategy should aim at maximising total profit and establishing a strong market presence, considering the detailed quantitative challenges and opportunities. Advanced Analysis Required : Apply the specific market characteristics data to tailor strategies for each market. Balance the supply constraints of Product Y with the boosted demand from complementary goods. Adjust the marketing strategy and budget allocation in response to global economic trends, particularly currency fluctuations. Mitigate the impact of competitor activities on market share and profit margins. |
|---|

First, let's ask plain ChatGPT to draw up a report of practical steps to be taken in response to this challenge.

| ChatGPT Executive Summary Objective : Maximise profit and establish a strong market presence for Product X and Product Y. Budget : $200,000 for the upcoming quarter. Focus : Balancing market characteristics, supply constraints, and global trends. Step-by-Step Action Plan Step 1 : Market Research and Analysis 1.1 : Conduct in-depth market research to identify key characteristics of each target market. 1.2 : Analyse competitors’ strategies in similar product launches. 1.3 : Gather data on cultural preferences, regulatory environments, and economic conditions. Step 2: Budget Allocation 2.1 : Allocate $90,000 for established markets, focusing on Product X. 2.2 : Allocate $80,000 for emerging markets, focusing on Product Y. 2.3 : Set aside $10,000 as a contingency fund for currency fluctuations and CSR initiatives. 2.4 : Reserve $20,000 for innovative marketing and countering competitor strategies. Step 3: Marketing Strategy Development 3.1 : Develop culturally tailored marketing campaigns for Product X in diverse markets. 3.2 : Plan complementary goods campaigns for Product Y in emerging markets. 3.3 : Design digital marketing campaigns to optimise ad spend and conversion rates. 3.4 : Implement CSR initiatives to enhance brand value and customer loyalty. Step 4: Regulatory Compliance and Market Entry 4.1 : Ensure compliance with local regulations in each market. 4.2 : Calculate and incorporate regulatory costs into the budget. 4.3 : Establish relationships with local partners for market entry and distribution . Step 5: Supply Chain Management 5.1 : Coordinate with the supply chain team to align production with market demands. 5.2 : Address supply constraints for Product Y, ensuring 60% demand fulfilment initially. 5.3 : Plan logistics for timely distribution in target markets. Step 6: Campaign Execution 6.1 : Launch marketing campaigns according to the tailored strategies. 6.2 : Monitor ad performance and conversion rates, adjusting strategies as necessary. 6.3 : Engage with customers through social media and other digital platforms. Step 7: Monitoring and Analysis 7.1 : Regularly review market responses and sales data. 7.2 : Adjust marketing and budget allocations based on performance and market feedback. 7.3 : Analyse currency fluctuations and adjust financial strategies accordingly. Step 8: Reporting and Feedback 8.1 : Prepare monthly reports on market performance, budget utilisation, and ROI. 8.2 : Gather team feedback and incorporate insights into future strategies. 8.3 : Present findings to stakeholders and adjust overall strategy for the next quarter. Conclusion Implementing this plan requires coordination across various departments, including marketing, sales, finance, and supply chain. Success hinges on adaptability, continuous analysis, and responsive strategy modification. Regular reviews and stakeholder engagement are essential to refine strategies and achieve the set objectives. |
|---|

This a low-quality response; only the information provided in Step 2 specifically addresses the original problem, the rest of ChatGPT's response is generic and wordy. Now let's use CoT Prompting together with Systems Analysis to solve the same problem.

First we'll get the Systems Question Rephraser GPT (https://t.ly/ax3tz) to rephrase the business problem from a systems analysis perspective; this gives the following output:

| Systems Analysis of the Problem: "Optimising International Product Launch Strategy with Quantitative Data" System Context: The system in question is a multinational company's marketing department, with the goal of launching two products (X and Y) in various international markets. The system encompasses elements such as budget allocation, market characteristics, product details, and external influences. Non-Active Elements : Budget Limitation : $200,000 for the marketing quarter. Product Characteristics : Product X and Product Y with distinct profit margins, conversion rates, and market sensitivities. Market Characteristics : Differentiating between emerging and established markets, each with unique growth potential, competitiveness, and cultural diversity . External Factors : Global economic trends (currency fluctuation), competitor activities, and sustainability/CSR initiatives. Active Elements : Marketing Department : Responsible for strategy formulation and budget allocation. Advertising Channels : Platforms for ad placements, influencing conversion rates and costs. Behaviours of Active Elements : Decision-making based on quantitative data analysis. Adjusting strategies in response to dynamic market conditions and external factors. Passive Elements : Regulatory environments and constraints. Supply limitations for Product Y. Internal Feedback Loops : The effectiveness of marketing strategies influencing future budget allocations and strategy modifications. The impact of market sensitivity and competitor activities on marketing approach. External Inputs and Outputs : Inputs : Market research data, global economic trends, competitor activities. Outputs : Marketing campaigns, budget expenditures, profits from sales. Initial State : Pre-launch phase with a defined budget but no allocated strategy. Intermediary States : Market Analysis : Assessing each market's characteristics and potential. Strategy Development : Tailoring strategies based on the analysis. Implementation : Executing the marketing plan. Final State : Successful launch of Products X and Y in targeted markets with optimised profit margins and market presence. Elements to Address : Data-Driven Strategy Formulation : Utilising quantitative data to inform marketing strategies. Budget Allocation : Distributing the budget efficiently across different markets and products. Supply-Demand Balance : Aligning supply constraints of Product Y with market demand. External Factor Mitigation : Adjusting strategies in response to economic trends and competition. Business Rules : Marketing expenditures should not exceed the allocated budget. Strategies must comply with local regulations and cultural sensitivities. Sustainability and CSR initiatives must be incorporated. Real-time adjustments should be made in response to currency fluctuations and competitor actions. Systems Requirements : Develop a marketing strategy that allocates the $200,000 budget effectively across different international markets for Products X and Y. Maximise total profit and establish strong market presence, considering quantitative challenges and opportunities. Apply market-specific data for tailored strategies in each market. Balance Product Y's supply constraints with demand, adjust strategies in response to global economic trends, and mitigate competitor impacts. |
|---|

Now we'll ask ChatGPT to draw up a precise report of steps that should be taken in practice in response to the original problem, using the specified systems approach.

This results in the following output.

| International Marketing Strategy Report Product X and Product Y Launch Budget: $200,000 Executive Summary This report outlines a strategic plan for launching Products X and Y in international markets, considering the unique characteristics of each product and market. The strategy leverages quantitative data to maximise profits and establish a strong market presence. 1. Budget Allocation and Market Focu s Product X Total Allocation: $120,000 (60% of total budget) Focus: Established Markets Key Actions : Digital Advertising: Allocate $80,000 for online advertising, focusing on high conversion regions. Cultural Customization: Reserve $24,000 (20% of Product X's budget) for adapting campaigns to cultural nuances. Regulatory Compliance: Set aside $16,000 for regulatory challenges. Product Y Total Allocation: $80,000 (40% of total budget) Focus: Emerging Markets Key Actions : Market Matching: Limit spending to $48,000 in line with the 60% supply constraint. Complementary Goods Partnerships: Invest $16,000 in local partnerships. Reserve Fund: Keep $16,000 for demand fluctuations and market opportunities. 2. Marketing Strategy Development Ad Campaigns: Develop targeted digital ad campaigns for both products, focusing on metrics like conversion rates and cost per click. Market Research: Conduct detailed research in each target market for cultural and regulatory insights. Performance Metrics: Establish key performance indicators (KPIs) for campaign monitoring. 3. Risk Management and Contingency Plannin g Currency Fluctuation Reserve: Allocate $10,000 (5% of total budget) for managing currency risks. Competitive Response Fund: Reserve $10,000 for marketing adjustments in response to competitor actions. 4. Sustainability and Corporate Social Responsibility (CSR) CSR Budget: Allocate $10,000 (5% of total budget) to CSR activities to enhance brand perception and loyalty. 5. Implementation Plan Month 1-2: Market research and campaign development. Month 3: Launch campaigns, with ongoing monitoring and adjustments. Month 4-6: Evaluate campaign effectiveness and adjust strategies as needed. 6. Monitoring, Evaluation, and Adjustment Data Analysis: Regularly analyse sales, market responses, and ad performance. Budget Reallocation: Adjust budget allocation based on performance data. Strategy Refinement: Modify strategies in response to market feedback and external factors. 7. Post-Launch Review and Reporting Review Meeting: Conduct a post-launch analysis to evaluate overall performance. Reporting: Document insights, successes, and areas for improvement. Conclusion This strategic plan leverages a systems approach to maximise the effectiveness of the $200,000 marketing budget. By tailoring strategies to each product and market, and by incorporating flexibility to adjust to real-time feedback and external factors, this plan aims to establish a strong market presence for Products X and Y, while also maximising profitability. This report provides a roadmap for the practical application of the systems approach to your international product launch, ensuring a data-driven, adaptable, and strategically sound execution. |
|---|

This CoT response is immeasurably better than the initial response when ChatGPT was presented with the original question alone.

It provides concrete action steps, precise suggestions for resource allocation and is better written in a compelling and interesting manner.

## Conclusion

The examples above demonstrate how we can get better AI responses using CoT Prompting together with a systems analysis approach.

This technique produces good results even in cases where it is not immediately obvious that the problems have anything to do with systems analysis at all.

---

# Section III - Copying the Experts

This section explores the possibilities of boosting AI output when solving problems, by using its ability to simulate expert personalities.

Learning from the experts, by ChatGPT

---

# Chapter 17. Expert Personality Simulation

The next section delves into using psychoanalytical techniques to boost AI performance, however, before using this approach, let's see if we can use a soft psychology approach to embellish the output from generative AI.

| The techniques presented in this chapter can be used in conjunction with CoT Prompting, but can also be used by themselves to good effect. |
|---|

## Simulating Personalities with ChatGPT

Generative AI's, such as ChatGPT, can simulate responses from different personas.

This can be amusing, for example:

| You As Henry VIII, compose an original Beatles song. Write it as if Henry VIII was transported through time and became one of the Beatles. ChatGPT Creating a song as if Henry VIII were transported through time and became a member of The Beatles offers an intriguing blend of historical and musical elements. Let's model the song in the style of "Help!" by The Beatles, known for its upbeat tempo and catchy melody: Title: "When I Ruled the World" (To the tune of "Help!" by The Beatles) (Verse 1) When I ruled the world, oh how things did whirl, In a Tudor spin, with a crown and a pearl. But now I'm here, in a time so new, Playing songs with the lads, under skies so blue. (Chorus) When I ruled, when I ruled, In a time so far and old. Now I sing, now I play, In a band that's just gold. (Verse 2) From my throne to the stage, it's been quite the change, In a world so wide, and at times so strange. With a guitar in hand, and a tune in my heart, I'm a king in a band, playing my part. (Bridge) In the courts of old, where the stories are told, I was mighty and bold, in the days of old. But here in this band, with a mic in my hand, I'm just one of the lads, in a rock 'n' roll land. (Chorus) When I ruled, when I ruled, In a castle, in the days of yore. Now I'm here, with a cheer, Up on stage, with a throne no more. |
|---|

Which is all very nice, but not very useful. Let's see if we can put ChatGPT's ability to simulate different personality types to better use.

[Imagen: Henry VIII (3) by Hans Holbein the Younger - PICRYL - Public Domain Media  Search Engine Public Domain Search]

Henry VIII by Hans Holbein the Younger, Public Domain

---

## Different Ways of Thinking

Different people see things in different ways, they also think in different ways.

Some people are naturally analytical, others are naturally more creative. In school, students excel in areas that suit their natural aptitudes, later they may choose careers that require their natural thinking styles.

- An analytical thinker might gravitate towards fields like engineering or data analysis.
- A creative thinker might find fulfilment in the arts or marketing, where innovation and out-of-the-box thinking are valued.

The following table lists some of the different cognitive (thinking) styles and their suitability to specific problem domains.

| Thinking Style | Description |
|---|---|
| Analytical | Characteristics: Logical, detail-oriented, and systematic. Suitability: Ideal for fields requiring precision and structured problem-solving, such as mathematics, engineering, and computer science. |
| Creative | Characteristics: Innovative, intuitive, and open-ended. Suitability: Beneficial in arts, design, marketing, and other fields where innovation and out-of-the-box solutions are crucial. |
| Critical | Characteristics: Questioning, sceptical, and evidence based. Suitability: Important in scientific research, law, and academia. Critical thinkers excel at evaluating arguments, identifying biases, and approaching problems with a healthy degree of scepticism. |
| Empathetic | Characteristics: Understanding, compassionate, and people oriented. Suitability: Empathetic thinkers are excellent at understanding human emotions and motivations, which is crucial in roles that involve working closely with people such as psychology, nursing, social work and customer service. |
| Holistic | Characteristics: Integrative, interconnected, and contextual. Suitability: Holistic thinkers are good at understanding systems, recognizing patterns, and considering the broader implications of problems and solutions. This is useful in disciplines like ecology and social sciences. |
| Practical | Characteristics: Realistic, application-focused, and pragmatic. Suitability: Practical thinkers are skilled at applying ideas in real-world scenarios and making decisions that are feasible and effective. This is essential for fields like business management and applied sciences. |
| Strategic | Characteristics: Big-picture oriented, long-term focused, and visionary. Suitability: Strategic thinkers are adept at anticipating future trends and making decisions that align with long-term goals. This is critical for roles in leadership, policy-making, and strategic planning. |

Since different types of problems benefit from the application of different thinking styles, it seems that we should be able to boost the output of generative AI, when solving problems, by asking the AI to simulate a personality with the thinking style best suited for the problem at hand.

The following chapters explore this avenue of thought.

---

# Chapter 18. Applying Specific Thinking Styles using AI

In addition to simulating specific personas, such as King Henry VIII, generative AIs, such as ChatGPT, can also simulate specific thinking styles.

Compare the following two conversations with ChatGPT-4.

### Without Specifying a Thinking Style

| You How can I take a beautiful photo on a rainy day in London? ChatGPT Taking a beautiful photo on a rainy day in London can be a delightful and artistic endeavour. Here are some tips to help you capture the unique beauty of a rainy day in the city: Embrace the Weather : Rain adds a dramatic and moody atmosphere to photos. Use the rain to your advantage to create more emotive and atmospheric images. Lighting : Overcast skies offer soft, diffused light which is great for photography. This kind of light reduces harsh shadows and can bring out the colors and details in your scene. Reflections : Look for puddles, wet streets, or any reflective surfaces. These can create beautiful and interesting reflections of cityscapes, landmarks, people, or lights. Umbrellas and Raincoats : People with colourful umbrellas and raincoats can add a pop of color and a human element to your photos. They can also give a sense of scale and context. Iconic Landmarks : Capture London's iconic landmarks like the Big Ben, Tower Bridge, or the London Eye. The rain can add a new perspective to these often-photographed sights. Street Photography : Rainy days are perfect for candid street photography. Capture people rushing by, walking under the rain, or interacting with the elements. Window Shots : If you prefer to stay dry, shooting through a window can give you a unique perspective. Raindrops on the window can add an interesting texture to your photo. Experiment with Shutter Speed : Playing with different shutter speeds can capture the rain in various ways. A fast shutter speed will freeze the raindrops, while a slower one can create a sense of motion. Post-Processing : Enhance your rainy day photos with post-processing. Adjust the contrast, saturation, and sharpness to bring out the best in your rainy day shots. Remember, the key to good photography is often about seeing things differently and capturing the mood of the moment. Rainy days in London offer a unique and charming setting, perfect for creating stunning and memorable photographs. |
|---|

Not a bad response, but also not very compelling. Let's see if we can do better.

### With Specifying a Particular Thinking Style

| You As a creative artist, how can I take a beautiful photo on a rainy day in London? ChatGPT Taking a beautiful photo on a rainy day in London offers a unique opportunity to capture the city's charm and moodiness. Here are some tips to help you make the most of this photographic opportunity: Embrace the Rain: Instead of seeing the rain as a hindrance, use it to your advantage. Rain can add a sense of drama and atmosphere to your photos. Look for reflections in puddles, raindrops on windows, and the way light plays with wet surfaces. Choose Your Subjects Wisely: Iconic London landmarks, like the Big Ben, London Eye, or Tower Bridge, can look even more striking under dark, moody skies. Streets lined with Victorian architecture, quaint alleyways, or bustling markets can also be compelling subjects in the rain. Lighting Considerations: Overcast skies diffuse sunlight, reducing harsh shadows and creating a soft light that's ideal for photography. If it's darker or in the evening, city lights can provide a warm, glowing contrast to the cool, wet environment. Use Color to Your Advantage: On a grey day, any splash of color – be it a red double-decker bus, colourful umbrellas, or people's clothing – can stand out strikingly. This contrast can add a dynamic element to your photos. Capture Movement: The hustle and bustle of London don’t stop for the rain. Capturing people hurrying under umbrellas, buses splashing through puddles, or even the rain itself, can add a dynamic element to your photographs. Experiment with Angles and Perspectives: Try shooting from different angles and perspectives. Low angles can be great for capturing reflections in puddles, while higher angles can provide a unique view of rain-soaked streets. Post-Processing: In post-processing, you can enhance the mood by adjusting the white balance, increasing contrast, or even converting images to black and white for a more dramatic effect. Patience is Key: Sometimes, waiting for the right moment can make all the difference – a sudden break in the clouds, a person walking into the perfect spot, or a change in the intensity of the rain. Enjoy the Process: Lastly, don't forget to enjoy the process. Exploring London in the rain can be a beautiful experience, and this will often come through in your photographs. Remember, the most important aspect of photography is your unique vision and creativity. Use the rainy day not as a limitation, but as an inspiration to see and capture London in a way that's unique to you. |
|---|

The difference between these two responses is subtle, but important.

For instance, compare:

"1. Embrace the Weather: Rain adds a dramatic and moody atmosphere to photos. Use the rain to your advantage to create more emotive and atmospheric images."

To:

"1. Embrace the Rain: Instead of seeing the rain as a hindrance, use it to your advantage. Rain can add a sense of drama and atmosphere to your photos. Look for reflections in puddles, raindrops on windows, and the way light plays with wet surfaces."

The second answer provides specific guidance and advice, which is more instructive than the general advice in the first response.

Additionally, the following advice given in the second conversation, is absent entirely from the first response:

"4. Use Color to Your Advantage: On a grey day, any splash of color - be it a red double-decker bus, colourful umbrellas, or people's clothing - can stand out strikingly. This contrast can add a dynamic element to your photos.

5. Capture Movement: The hustle and bustle of London don't stop for the rain. Capturing people hurrying under umbrellas, buses splashing through puddles, or even the rain itself, can add a dynamic element to your photographs."

By specifying the thinking style that is best suited to answer our question, we get a much better result from ChatGPT.

Trafalgar Square in the rain, by ChatGPT

---

# Chapter 19. Combining Thinking Styles

In addition to specifying one specific thinking style to address a problem, we can also get an AI, such as ChatGPT, to apply various thinking styles in order to address a single problem from different perspectives.

This simulates team thinking, where each person contributes by applying their own specific thinking style to the problem at hand. For example:

| Case Study: Urban Food Desert Background : In a large urban area, there are several "food deserts" – neighbourhoods with limited access to affordable and nutritious food. The closest supermarkets are several miles away, and many residents, especially those with low income or without cars, struggle to find healthy food options. This issue is compounded by a lack of green spaces and high rates of obesity and health problems related to poor diet. Goal : To develop and implement a comprehensive, sustainable solution that not only addresses the immediate issue of food accessibility but also contributes positively to the overall health and well-being of the community in the long term. Relevant Data Food Accessibility and Health : Grocery Store Locations : 15 grocery stores, 10 markets, 5 community food pantries. Accessibility : Average distance from food deserts to nearest grocery store is 4.5 miles. Obesity Rates : 35% in food desert areas vs. 20% city average. Diabetes Prevalence : 12% in food desert areas, above city average of 8%. Demographics and Community Insights : Population Density : 12,000 people per square mile in food desert areas. Income Levels : Median household income in food deserts is $25,000, compared to city average of $55,000. Vehicle Ownership : 40% households own a vehicle, against city average of 70%. Community Feedback : Preferences for mobile food markets, community gardens, and subsidized grocery memberships. Community Profiles : Diverse ethnic backgrounds, with 60% non-English speakers. Innovative Solutions and Case Studies : Innovation Trends : Automated mobile grocery stores, hydroponic urban farms, community-supported agriculture. Successful Models : Cities with urban farming initiatives reducing food desert impacts by 30%. Financial and Operational Planning : Budget : $500,000 initial investment for mobile markets, $200,000 annual maintenance. Logistics : Identified areas for mobile markets and urban farms. Resource Availability : Partnerships with two local nonprofits, 50 committed volunteers. Policy and Strategic Planning : Policy Landscape : Current restrictions on urban farming and mobile food vendors. Funding Sources : Identified grants totalling $350,000, potential local business sponsorships. Sustainability Projections : Aim to become self-sustaining within 5 years. Risk Management and Community Engagement : Impact Assessment : 25% improvement in healthy eating habits from similar interventions. Risks : Low initial participation, spoilage of produce, zoning issues. Feedback Mechanisms : Online surveys, quarterly community meetings, feedback boxes. Cultural and Inclusive Approaches : Community Needs : Demand for affordable, culturally appropriate produce, and nutrition education. Cultural Considerations : Preference for fresh vegetables and grains, dietary practices. Inclusion Strategies : Community advisory board with diverse representation, multilingual materials, accessible locations. |
|---|

Urban Food Desert, by ChatGPT

---

First, let's ask generic ChatGPT to solve the Urban Food Desert problem without specifying what thinking styles should be applied.

| You Solve this problem: Problem: Urban Food Desert Resolution Background: In a large urban area, ... ChatGPT Addressing the problem of urban food deserts requires a multifaceted approach that integrates community engagement, innovative solutions, financial planning, policy advocacy, and cultural inclusivity. Here's a comprehensive plan to tackle this issue: 1. Community Engagement and Feedback Establish a community advisory board with diverse representation to ensure the initiatives cater to the specific needs and preferences of the community. Conduct regular community meetings and online surveys to gather feedback and adapt strategies accordingly. Implement educational programs focused on nutrition and healthy eating, using multilingual materials to reach non-English speakers. 2. Innovative Solutions for Food Accessibility Deploy automated mobile grocery stores to travel through food desert areas, providing access to affordable and nutritious food. Develop hydroponic urban farms in available green spaces to grow fresh produce locally. Promote community-supported agriculture (CSA) programs where residents can subscribe for regular deliveries of fresh produce. 3. Financial and Operational Planning Utilize the initial investment of $500,000 for setting up mobile markets and $200,000 for annual maintenance. Explore partnerships with local businesses for sponsorship opportunities and additional funding. Identify and prepare locations for mobile markets and urban farms, considering accessibility for residents without vehicles. 4. Policy and Strategic Planning Advocate for changes in urban farming and mobile food vendor policies to support these initiatives. Secure funding through identified grants and potential sponsorships to ensure financial sustainability. Aim to become self-sustaining within 5 years through the sale of produce and community support. 5. Risk Management Plan for risks such as low initial participation, produce spoilage, and zoning issues. Implement strategies to increase community participation, such as incentives or loyalty programs. Regularly assess the impact of interventions and adjust strategies as needed. 6. Cultural and Inclusive Approaches Offer a range of culturally appropriate produce and dietary options, catering to the diverse ethnic backgrounds of the community. Ensure locations for mobile markets and urban farms are accessible and inclusive for all residents. Provide nutrition education that respects and incorporates cultural dietary practices. 7. Monitoring and Evaluation Track improvements in access to healthy food and changes in health metrics like obesity and diabetes rates. Use feedback mechanisms like community meetings and online surveys to evaluate the effectiveness of interventions. Adjust and scale up successful strategies based on data-driven insights. 8. Long-term Community Development Foster a sense of community ownership and involvement in the initiatives to ensure their longevity. Encourage local entrepreneurship opportunities related to urban farming and healthy food retail. Continuously engage with community leaders and residents to ensure the solutions evolve with the community's needs. This comprehensive approach aims to not only address the immediate issue of food accessibility but also contribute positively to the overall health and well-being of the community in the long term. By involving the community at every step, leveraging innovative solutions, and strategically planning for sustainability and inclusivity, the urban food desert problem can be effectively mitigated. |
|---|

Now let's see what happens if we ask ChatGPT to apply relevant expert thinking styles to the problem at hand.

First, let's find the required types of expert needed to solve the problem.

| You Identify roles that would be required to solve this problem: "Problem: Urban Food Desert Resolution Background: In a large urban area…. " Using these types of thinking: Analytical Thinking Creative Thinking Practical Thinking Strategic Thinking Holistic Thinking Critical Thinking Empathetic Thinking Don’t solve the problem, simply identify the required roles. ChatGPT To address the complex problem of urban food desert resolution, a variety of roles are required, each employing different types of thinking: Urban Planners (Strategic Thinking, Holistic Thinking): To design and implement effective layouts for urban farms, mobile markets, and community gardens. They consider zoning laws, accessibility, and optimal use of space. Nutritionists and Health Experts (Analytical Thinking, Empathetic Thinking): To guide the selection of nutritious food offerings, focusing on the health needs and dietary practices of the community. Community Outreach Coordinators (Empathetic Thinking, Practical Thinking): To engage with the community, gather feedback, and ensure that solutions are culturally appropriate and inclusive. Agricultural Experts and Urban Farmers (Creative Thinking, Practical Thinking): To develop and manage urban farming initiatives, including hydroponic farms, ensuring sustainable and efficient food production. Logistics and Supply Chain Managers (Analytical Thinking, Practical Thinking): To oversee the distribution of food through mobile markets, ensuring that fresh produce reaches residents effectively. Policy Analysts and Advocates (Strategic Thinking, Critical Thinking): To navigate and influence the policy landscape, addressing restrictions on urban farming and mobile food vendors. Financial Planners and Grant Writers (Analytical Thinking, Strategic Thinking): To manage the budget, secure funding through grants and sponsorships, and ensure long-term financial sustainability. Risk Management Specialists (Critical Thinking, Analytical Thinking): To identify potential risks such as low participation or spoilage of produce and develop strategies to mitigate them. Marketing and Public Relations Professionals (Creative Thinking, Empathetic Thinking): To promote the initiatives, raise public awareness, and drive community participation. Data Analysts and Researchers (Analytical Thinking, Critical Thinking): To collect and analyse data on food accessibility, health outcomes, and community feedback, informing ongoing improvements. Technology and Innovation Specialists (Creative Thinking, Strategic Thinking): To explore and implement innovative solutions like automated mobile grocery stores and community-supported agriculture platforms. Community Educators and Trainers (Empathetic Thinking, Practical Thinking): To provide nutrition education and training to the community, focusing on healthy eating habits and sustainable practices. Volunteer Coordinators (Practical Thinking, Empathetic Thinking): To manage and mobilize volunteers, ensuring effective participation in various initiatives. Cultural Liaisons (Empathetic Thinking, Holistic Thinking): To ensure that the diverse cultural needs and preferences of the community are met, particularly for non-English speakers. Each role leverages different types of thinking to collectively create a comprehensive, sustainable solution to the urban food desert problem. |
|---|

Now let's ask ChatGPT what each of these expert roles can contribute to resolving the Urban Food Desert problem.

| You Address the following problem from the discrete perspectives of each of the following roles: 1. Urban Planners. 2. Nutritionists and Health Experts. 3. Community Outreach Coordinators. 4. Agricultural Experts and Urban Farmers. 5. Logistics and Supply Chain Managers. 6. Policy Analysts and Advocates. 7. Financial Planners and Grant Writers. 8. Risk Management Specialists. 9. Marketing and Public Relations Professionals. 10. Data Analysts and Researchers. 11. Technology and Innovation Specialists. 12. Community Educators and Trainers. 13. Volunteer Coordinators. 14. Cultural Liaisons. Problem Statement: Urban Food Desert Resolution Background: In a large urban area... ChatGPT Let's address the urban food desert issue by providing concrete solutions from the perspective of each professional role, using the supplied data: Urban Planners : Redesign city plans to allocate specific areas for community gardens and urban farms, considering the high population density. Implement pedestrian-friendly routes and bike lanes to the existing grocery stores, reducing the 4.5 miles distance barrier for residents without cars. Nutritionists and Health Experts : Develop a targeted nutritional education program focusing on the areas with 35% obesity rates and 12% diabetes prevalence. Collaborate with local markets to offer cooking classes and health seminars, emphasizing affordable, healthy eating. Community Outreach Coordinators : Organize community meetings and workshops in diverse languages, catering to the 60% non-English speaking population. Gather feedback on the preferred solutions like mobile markets and community gardens, ensuring their implementation aligns with community needs. Agricultural Experts and Urban Farmers : Set up urban farming initiatives in designated green spaces, focusing on crops that are culturally relevant and easy to grow in the urban environment. Provide training to local residents to manage these spaces, creating a sustainable source of fresh produce. Logistics and Supply Chain Managers : Develop a robust distribution network for the mobile markets, ensuring they regularly visit the food desert areas. Coordinate with local farmers and markets to maintain a consistent supply of fresh produce, considering the low vehicle ownership in these areas. Policy Analysts and Advocates : Work on amending current urban farming and mobile food vendor restrictions. Advocate for policies that support food accessibility initiatives and lobby for increased funding from the identified grants and local business sponsorships. Financial Planners and Grant Writers : Create a detailed budget plan for the $500,000 initial investment and $200,000 annual maintenance, ensuring the effective allocation of resources. Secure additional funding through grant applications and partnerships with local businesses. Risk Management Specialists : Develop strategies to mitigate risks like low participation and produce spoilage. Implement a pilot program to test the mobile market concept and adjust based on early feedback, considering the potential zoning issues. Marketing and Public Relations Professionals : Launch a multilingual marketing campaign to promote the new food accessibility initiatives, focusing on their benefits to health and community well-being. Use local success stories to build trust and encourage participation. Data Analysts and Researchers : Track and analyse data on changes in obesity and diabetes rates in the target areas. Measure the impact of the implemented solutions on food accessibility and community health, providing insights for continuous improvement. Technology and Innovation Specialists : Explore the integration of innovative solutions like automated mobile grocery stores or hydroponic urban farms. Implement technology to optimize the distribution routes of mobile markets and track the usage patterns of community gardens. Community Educators and Trainers : Offer multilingual education programs on nutrition and sustainable gardening practices. Conduct workshops on healthy cooking techniques that are affordable and culturally appropriate, addressing the diverse community profiles. Volunteer Coordinators : Recruit and manage the 50 committed volunteers, assigning them roles in urban farming projects, community outreach, and educational workshops. Develop a volunteer training program to ensure effective and meaningful participation. Cultural Liaisons : Engage with different cultural groups within the community to ensure the solutions are culturally sensitive. Facilitate the creation of culturally appropriate educational materials and ensure the availability of diverse produce that meets the community's dietary preferences. Each role's solution contributes to a comprehensive strategy to combat the challenges of urban food deserts, ensuring the initiatives are sustainable, culturally sensitive, and effectively address the community's needs. |
|---|

If we look at the actual practical advice given by ChatGPT via each of these methods, we see the following differences.

Community Engagement

Both the unstructured and structured methods gave advice to involve the community to better understand their needs.

Actionable Advice

Besides community engagement, the unstructured ChatGPT response only gave one piece of immediately actionable advice.

| 2. Innovative Solutions for Food Accessibility : Deploy automated mobile grocery stores to travel through food desert areas, providing access to affordable and nutritious food. Develop hydroponic urban farms in available green spaces to grow fresh produce locally. Promote community-supported agriculture (CSA) programs where residents can subscribe for regular deliveries of fresh produce. |
|---|

The Specific Thinking Styles method, however, offered the following:

| 1. Urban Planners : Redesign city plans to allocate specific areas for community gardens and urban farms, considering the high population density. Implement pedestrian-friendly routes and bike lanes to the existing grocery stores, reducing the 4.5 miles distance barrier for residents without cars. 2. Nutritionists and Health Experts : Develop a targeted nutritional education program focusing on the areas with 35% obesity rates and 12% diabetes prevalence. Collaborate with local markets to offer cooking classes and health seminars, emphasizing affordable, healthy eating. 4. Agricultural Experts and Urban Farmers : Set up urban farming initiatives in designated green spaces, focusing on crops that are culturally relevant and easy to grow in the urban environment. Provide training to local residents to manage these spaces, creating a sustainable source of fresh produce. 5. Logistics and Supply Chain Managers : Develop a robust distribution network for the mobile markets, ensuring they regularly visit the food desert areas. Coordinate with local farmers and markets to maintain a consistent supply of fresh produce, considering the low vehicle ownership in these areas. 11. Technology and Innovation Specialists : Explore the integration of innovative solutions like automated mobile grocery stores or hydroponic urban farms. Implement technology to optimize the distribution routes of mobile markets and track the usage patterns of community gardens. |
|---|

In other words, the structured method attacked the problem from various angles and offered various ways to progress the situation. The unstructured method only offered one piece of immediately actionable advice, which does not translate to a real plan of action.

By first finding the required experts (using ChatGPT) and then asking ChatGPT to solve the problem from the perspectives of each of these experts, we were able to get a far superior and useful response.

Saved from starvation, by ChatGPT

# Chapter 20. Invoking Specific SMEs (Subject Matter Experts)

In addition to generic expert roles, we can ask ChatGPT to simulate the responses of known individual experts when responding.

Let's apply this technique to design a software solution, using specific industry experts to address different aspects of a software solution, as follows:

- Steve Jobs , for elegant GUI design.
- Jeff Bezos , for business strategy.
- A consultant from Capgemini , for system architecture.

### Case Study: Website for Custom Travel Experiences Company

Let's say that a company that specialises in custom travel experiences wants to update their website, and they have engaged the services of a Business Analyst to compile their requirements into a document (called a Technical Solution Document) that can be used by the programmers to develop the new website.

The Business Analyst is faced with the following problem statement.

| Company Overview Active Escape Solutions is a company specializing in technology solutions for travel and leisure. AES focuses on delivering personalised, activity-based travel experiences by leveraging real-time data on weather conditions, user-specific exercise preferences, and local recreational offerings . Current Scenario and Trends AES has identified a growing market demand for tailored travel experiences, especially among individuals seeking active, health-conscious getaways. The trends fuelling this growth include an increased focus on personal wellness, the popularity of outdoor activities, and the desire for customised travel planning based on real-time data. AES's platform caters to these needs by integrating weather forecasting, personal fitness data, and local tourism information. Challenges and Goals AES aims to revolutionise the travel planning experience by providing a seamless, intuitive platform where users can find the best destinations for active weekends away. The current AES website faces issues like limited user interaction, inconsistent data integration, and a need for real-time, activity-specific information. The existing system faces challenges such as: Limited customization in travel planning. Inconsistency in data integration, leading to suboptimal destination recommendations. Inadequate access to comprehensive, real-time information on weather and local offerings. Challenges in engaging with users who seek detailed, activity-specific information. Project Scope for the New System The development of a web-based platform to recommend ideal travel destinations, integrating various data points, and ensuring a seamless user experience . Specifically the development of a web-based platform that: Integrates real-time weather data, user exercise preferences, and local tourism offers to recommend ideal active weekend destinations. Provides a user-friendly interface for personalised travel planning. Ensures data consistency and accuracy through a unified, robust backend system. Offers detailed information about various activities and destinations. Supports multilingual access. Includes features for direct booking and itinerary customization. Exclusions from Project Scope The project will not cover: Creation of the content for the recommended destinations, which will be sourced from external partners. Development of the underlying weather forecasting and personal fitness tracking technologies. Management of actual travel logistics such as transportation and accommodation bookings. Development of a comprehensive customer relationship management (CRM) system. The new system aims to position AES as a leader in the market of active, personalised travel experiences. |
|---|

First, the Business Analyst asks generic ChatGPT to write a Technical Solution Document for the AES problem statement, by simply specifying the problem statement:

| You Write a Technical Solution Document for the following project. Address architecture related issues, usability issues and the business perspective of the project separately:... ChatGPT Technical Solution Document for Active Escape Solutions' New Web-based Platform 1. Introduction 1.1 Company Overview Active Escape Solutions (AES) specialises in advanced technology solutions for travel and leisure, focusing on delivering personalised, activity-based travel experiences. AES leverages real-time data on weather conditions, user-specific exercise preferences, and local recreational offerings. 2. Current Scenario and Market Trends Market Demand : Growing demand for tailored travel experiences, particularly among health-conscious individuals. Trends : Increased focus on personal wellness, popularity of outdoor activities, and desire for customised travel planning. AES’s Role : AES integrates weather forecasting, personal fitness data, and local tourism information. 3. Challenges and Goals Limited User Interaction : Need for enhanced direct user interaction and customization. Data Integration Issues : Inconsistency in data integration affects destination recommendations. Information Accessibility : Inadequate real-time information on weather and local offerings. User Engagement : Challenges in engaging users seeking detailed, activity- specific information. 4. Project Scope New System Features : Integration of real-time weather data, user preferences, and local tourism offers. User-friendly interface for personalised travel planning. Data consistency and accuracy through a unified backend. Detailed information on activities and destinations. Multilingual access. Direct booking and itinerary customization. Exclusions : Content creation for destinations. Development of weather forecasting and fitness tracking technologies. Management of travel logistics. Development of a comprehensive CRM system. 5. Technical Solution 5.1 System Architecture Frontend : Responsive design using modern web frameworks. Backend : Robust server architecture with efficient data processing capabilities. Database : Scalable database for handling diverse datasets. API Integration : Seamless integration with external APIs for real-time data. 5.2 Usability Issues and Solutions User Interface : Intuitive and interactive UI/UX design. Accessibility : Compliance with accessibility standards. Personalization : Advanced algorithms for personalised recommendations. Multilingual Support : Language options for global accessibility . 5.3 Business Perspective Market Positioning : Establishing AES as a leader in personalised travel experiences. User Engagement : Increasing user retention through customised offerings. Data Utilisation : Leveraging data for informed business decisions. Partnerships : Collaborating with local tourism boards and fitness platforms. 6. Development and Implementation Plan Requirement Analysis : Understanding user needs and market demands. Design and Architecture Planning : Creating a scalable and robust system design. Development Phases : Iterative development with continuous feedback integration. Testing and Quality Assurance : Ensuring reliability and performance. Deployment and Monitoring : Launching the platform with ongoing monitoring. 7. Conclusion The proposed system aims to revolutionise the travel planning experience, addressing the current challenges and aligning with AES's business goals. Through this initiative, AES is poised to become a key player in the niche market of active, personalised travel experiences. |
|---|

The Business Analyst despairs at ChatGPT's weak response. Besides regurgitating the original problem statement, ChatGPT added virtually no specific actionable information.

Subsequently the Business Analyst changes their AI prompt and asks ChatGPT to simulate subject-matter experts to address each aspect of the problem.

| You Write a technical solution document for the following project. Address architecture related issues as a consultant from Capgemini. Address usability issues as Steve Jobs. Address the business perspective of the project as Jeff Bezos:... ChatGPT Technical Solution Document for Active Escape Solutions (AES) 1. Introduction Company Overview Active Escape Solutions (AES) specialises in advanced technology solutions for travel and leisure, focusing on delivering personalised, activity-based travel experiences by leveraging real-time data on weather conditions, user exercise preferences, and local recreational offerings. 2. Current Scenario and Trends AES is responding to a growing market demand for tailored travel experiences, driven by a focus on personal wellness, outdoor activities, and customised travel planning based on real-time data. 3. Challenges and Goals AES aims to revolutionise travel planning with a seamless, intuitive platform. Current challenges include limited user interaction, inconsistency in data integration, and inadequate real-time information access . 4. Project Scope The project involves developing a web-based platform that integrates real-time weather data, user preferences, and local tourism offers, providing a user-friendly interface with data consistency, detailed information, multilingual support, and booking features. Exclusions from Project Scope The project excludes content creation for destinations, development of weather and fitness technologies, management of travel logistics, and CRM system development. 5. Architecture Perspective (Capgemini Consultant) System Architecture and Integration Microservices Architecture: Adopt a microservices architecture for scalability and flexibility. Each service (weather data, user preferences, local offers) should operate independently yet integrate seamlessly. API-First Approach: Design with an API-first approach to ensure interoperability and ease of integration with external data sources and services. Cloud Infrastructure: Utilise cloud-based solutions for scalability, reliability, and global reach. Implement solutions like AWS or Azure for efficient data storage and processing. Data Management and Security Data Warehousing: Implement a robust data warehousing solution to handle large volumes of data while ensuring quick access and data integrity. Security and Compliance: Prioritise security measures and comply with international data protection regulations, considering the global nature of the service. 6. Usability Perspective (Steve Jobs) User Interface and Experience Simplicity and Intuitiveness: Focus on a clean, intuitive interface. Every element should serve a purpose and enhance the overall user experience. Personalization: Implement dynamic personalization to make users feel understood and valued. Responsive Design: Ensure the platform is responsive and accessible across various devices and platforms. Engagement and Interaction User Feedback Loop: Integrate mechanisms for user feedback to continuously improve user experience. Visual Aesthetics: Emphasise visual aesthetics for a more engaging and delightful user experience. 7. Business Perspective (Jeff Bezos) Market Positioning and Growth Strategies Focus on Customer Experience: Prioritise customer satisfaction to drive growth. Use data analytics to understand and predict customer preferences. Innovative Features: Introduce innovative features like AI-based destination recommendations to differentiate AES in the market. Revenue and Expansion Monetization and Partnerships: Explore monetization through premium features and partnerships with local tourism authorities. Global Expansion: Strategically expand to new markets, considering multilingual and multicultural aspects for broader appeal . Branding and Customer Engagement Brand Building: Strengthen AES's brand as a leader in personalised travel experiences. Targeted Marketing: Utilise targeted marketing strategies to reach potential users, emphasising the unique value proposition of AES. 8. Conclusion This new system for AES is poised to redefine the landscape of personalised travel planning. By addressing architectural robustness, user-centric design, and strategic business positioning, AES will establish itself as a frontrunner in delivering personalised, activity-based travel experiences. |
|---|

In this response, ChatGPT has provided numerous avenues of exploration and pointers to specific methods and technologies that can be used to achieve AES's aims.

By leveraging specific SMEs, the Business Analyst has obtained a far superior output from ChatGPT.

Note: In their prompt, the Business Analyst used a combination of a generic expert persona (a consultant from Capgemini), together with specific individual expert personas (Steve Jobs and Jeff Bezos).

A Discussion, by ChatGPT

---

# Chapter 21. A Subject Matter Expert GPT

In addition to specifying particular subject matter experts as demonstrated in the previous chapter, we can automate the process of finding specific individual SMEs (subject matter experts) and then virtually consulting with them, using a GPT.

This GPT - Triple Advisor (https://t.ly/EyplK)- looks up relevant SMEs in the field that relates to the question, and then asks them to answer the question posed by the user.

| You Should I try to climb the corporate ladder or should I follow my heart? Triple Advisor I did a quick search and here's what I found. Your question about whether to climb the corporate ladder or follow your heart in your career path is complex and subjective. It involves balancing personal passions and practical considerations. To provide a well-rounded perspective, I've consulted insights from three experts with distinct viewpoints on this topic: Dr. Alan M. Patterson , an organizational development consultant; Jim Yong Kim , former President of Dartmouth College and the World Bank; and a team of McKinsey researchers, including Joanna Barsh, Marla M. Capozzi, and Jonathan Davidson , who focus on leadership and innovation. Intellectual Analysis - Dr. Alan M. Patterson : Dr. Patterson emphasizes that the traditional corporate ladder is increasingly outdated in today's rapidly changing and uncertain economic environmen t ​ ​ . He notes that the idea of a meritocracy in climbing the corporate ladder is often a myth, with many variables affecting one's ability to ascen d ​ ​ . Patterson suggests that rather than focusing on climbing the ladder, individuals should take control of their career development and seek meaningful work that aligns with their personal motivation s ​ ​ . He encourages a shift from self-centered career advancement to building organizational capacity and fostering relationships for broader impac t ​ ​ . Leadership Perspective - Jim Yong Kim : Jim Yong Kim advocates for young leaders to find their passion and aspire to make significant changes in their chosen field s ​ ​ . He acknowledges the scepticism around following one's passion, especially considering financial constraints and practical life concern s ​ ​ . Kim argues against the false binary of passion vs. practicality, suggesting that one can find meaningful work that is also financially sustainabl e ​ ​ . He encourages a balance between pursuing one's passion and practical considerations, emphasizing the importance of aligning career choices with personal values and the impact one wishes to mak e ​ ​ . Innovation and Change Perspective - McKinsey Researchers (Barsh, Capozzi, Davidson) : The McKinsey team observes that innovation is a key driver of growth in organizations, but there's a gap between aspirations and the ability to execute innovative idea s ​​​ ​ . They highlight the importance of organizational culture and leadership in driving innovation, suggesting that traditional structures and processes are not sufficien t ​​​ ​ . Their research suggests that leadership plays a crucial role in fostering an environment conducive to innovation, with a focus on trust, risk-taking, and openness to new idea s ​ ​ . The team recommends practical steps for leaders to encourage innovation, including defining innovation goals, integrating innovation into strategic agendas, and creating opportunities for experimentatio n ​ ​ . In summary, Dr. Alan M. Patterson's intellectual analysis points to the limitations of the traditional corporate ladder and advocates for a more self-directed approach to career development focused on meaningful work. Jim Yong Kim's leadership perspective emphasizes the importance of passion in one's career but acknowledges the need to balance this with practical considerations. The McKinsey researchers offer an innovative and change-driven viewpoint, stressing the role of leadership and organizational culture in driving innovation and growth. The decision to climb the corporate ladder or follow your heart should consider these diverse perspectives, aligning your personal values, passions, and practical needs to forge a fulfilling career path. |
|---|

This is a far more informed and interesting response than the vanilla ChatGPT answer to this question:

| You Should I try to climb the corporate ladder or should I follow my heart? ChatGPT Deciding whether to climb the corporate ladder or follow your heart is a deeply personal decision and depends on various factors unique to your life. Here are some aspects to consider: Personal Values and Goals : Reflect on what's truly important to you. If success, financial security, and career advancement align with your values, climbing the corporate ladder might be fulfilling. However, if you have passions outside this path that resonate more with your core values, following your heart might be more satisfying. Financial Stability : Consider your financial needs and responsibilities. Climbing the corporate ladder often offers more financial stability and benefits. If you have significant financial obligations or goals, this might be an important factor. Long-Term Fulfilment : Think about where you see yourself in the future. Corporate success can bring satisfaction, but so can pursuing a passion. Which path aligns more with your long-term vision for happiness and fulfilment? Risk Tolerance : Following your heart might involve more risks, such as less stable income or the uncertainty of success in a less conventional path. Assess how comfortable you are with these risks. Work-Life Balance : Consider the kind of work-life balance each path offers. Corporate careers can be demanding, potentially impacting personal time and relationships. Conversely, following your passion might offer more flexibility but could also require significant time and energy, especially in the early stages. Potential for Regret : Sometimes, the fear of regret can guide your decision. Would you regret not pursuing a corporate career, or would you regret not following your passion? Seek Advice : Talk to mentors, peers, or professionals who have faced similar choices. Their insights can provide valuable perspectives. Experiment and Reflect : If possible, try to engage in your passion alongside your current career. This might provide clearer insights into what you truly want. Personal Growth and Development : Each path offers different opportunities for personal growth. Which aligns more with your desire for personal development? Happiness and Stress Levels : Consider the impact of each choice on your mental health and overall happiness. Remember, there's no right or wrong answer. It's about what feels right for you, taking into account your circumstances, values, and aspirations. Sometimes, a balanced approach, where you maintain a stable job while exploring your passions, can also be a viable path. |
|---|

Note: The types of experts searched for by the Triple Advisor GPT is based on psychoanalytical theory presented later in this book (see the chapter on Systems Abstraction of Transactional Analysis).

---

# Section IV - Introduction to Psychoanalysis

This section gives a high level overview of Transactional Analysis, a school of psychoanalysis. The next section explains how we can use Transactional Analysis together with Chain of Thought Prompting to simulate human thought.

On the psychoanalyst's couch, by ChatGPT

---

# Chapter 22. Combining Psychoanalysis with AI

## Psychoanalysis

Psychoanalysis, invented by Sigmund Freud, divides human behaviour and thoughts into their component elements. Based on this analysis, psychoanalysis aims to provide people with tools and techniques to better understand their thoughts and feelings, and so achieve harmony in their everyday lives.

Some of the ways in which psychoanalysis segments human psychology are as follows:

- The Unconscious : Psychoanalysis delves into the unconscious mind, where it seeks to uncover and segment hidden thoughts, feelings and motivations.

- Dissecting Complex Behaviours : Psychoanalysis views human behaviour as the result of multiple, interrelated, psychological processes. By segmenting these behaviours into basic elements, psychoanalysis aims to understand and address the root causes of behavioural and mind-based issues.

- Analysing Thought Processes : Individual thoughts are seen as a complex amalgamation of conscious and unconscious processes, memories, and internalised experiences.

Psychoanalysis breaks down these thought processes to better understand how past experiences and learned thinking patterns shape an individual's thinking and behaviour.

This analysis allows for a deeper understanding of the underlying mechanisms of the psyche, and aims to bring about greater self-awareness and psychological health.

## Simulating the Human Mind using AI

Assuming that the human mind is structured in the most efficient way possible, leads us to the idea that if we can simulate the way that the mind uses different thought-processing centres in AI, then we can increase the efficiency and power of the AI simply by following the structure of the human thought process, without increasing the power of the underlying AI model.

In other words, we can use psychoanalytical techniques in conjunction with Chain of Thought Prompting to simulate the human mind. Thereby we can enhance AI's problem-solving and analytical abilities and develop AI systems that can approximate human-like reasoning and decision-making.

This approach does not require an increase in computational power but instead leverages the efficient structural and functional architecture of the human mind.

The possibilities of this approach are explored in the current and following sections.

Exploring the patterns of nature, by ChatGPT

---

# Chapter 23. Introduction to Transactional Analysis

Transactional Analysis is a psychoanalytical theory for understanding human behaviour in a structured and systematic way.

Transactional Analysis is used in various fields such as education, organisational management, and counselling for better understanding and management of personal and social dynamics.

## Suitability of Transactional Analysis for Generative AI

Out of the various schools of psychoanalysis, Transactional Analysis (TA) stands out as being particularly well suited for use with generative AI, for the following reasons:

- Clear Psyche Structure : Transactional Analysis has a well-defined and clear model of the psyche, introducing concepts like ego states (Parent, Adult, Child) and sub ego states (which are further divisions of the primary ego states). The well-defined TA model of the psyche gives the AI a clear basis for its psychoanalysis.
- Patterns of Communication : Transactional Analysis focuses on clarifying the actual meaning of patterns of communication. These well-defined patterns provide a clear framework for AI to analyse and interpret.
- Language-Based Approach : Unlike other psychoanalytical schools that use imagery and symbolic interpretation, Transactional Analysis primarily relies on spoken communication for analysing psychological processes. This focus on language aligns well with the NLP (natural language processing) capabilities of generative AI.

Insummary, Transactional Analysis, with its well-defined model of the psyche and clear interpretations of interpersonal communication, presents an ideal psychoanalytical school for application via AI. This is because the methodological structure of Transactional Analysis aligns with AI's key strengths in systematic analysis and natural language processing.

## Main Areas of Transactional Analysis

The main areas of Transactional Analysis are as follows:

### Structural Analysis

Structural Analysis is that area of TA which analyses the internal structure of the human mind. TA Structural Analysis breaks down the personality into three distinct ego states: Parent ego state, Adult ego state, and Child ego state.

Each ego state represents a self-contained system of thoughts, feelings, and behaviours.

- The Parent ego state thinks in the same way as the person's actual parents and parent figures, such as teachers.

- The Adult ego state is the home of the faculty of rational thought, and responds logically based on current reality.

- The Child ego state is the seat of feeling, and tends to reflect the patterns of emotion experienced in childhood.

Understanding these ego states helps in analysing how individuals think internally and how they interact with others.

Structural Analysis is explained in Chapter 14.

---

### Transactional Analysis (proper)

Transactional Analysis (proper) refers to the study of interactions, or 'transactions', between individuals. In this area of psychoanalysis, the focus is on identifying which ego states are involved in a transaction and how this influences the direction of the communication.

Transactional Analysis (proper) is a complex area of Transactional Analysis, and is discussed further in Chapter 15.

### Game Analysis

Games in Transactional Analysis are repetitive behaviours people engage in with others. These games often have hidden psychological motives and can lead to positive or negative outcomes.

Game Analysis helps in identifying these patterns, understanding their underlying motives, and assists people in finding ways to stop participating in negative games in favour of developing healthy relationships.

### Script Analysis

Script Analysis involves examining an individual's life plan or 'script', which is unconsciously developed in childhood and guides their behaviour and life choices. Scripts often have a deep impact on an individual's life story and can be either positive or limiting.

Script Analysis aims to uncover these scripts, understand how they influence current behaviour, and work towards rewriting limiting aspects of the script for a more fulfilling life plan.

## Further Reading

This book uses the TA ideas of Structural Analysis and Transactional Analysis (proper), and so presents a brief outline of these Transactional Analysis areas below. For further reading on Game Analysis and Script Analysis, the classics are Eric Berne's original books. Numerous other books and online resources are also available.

---

# Chapter 24. Structural Psychoanalysis

## Ego States

Ego states are a core concept in Transactional Analysis. According to Transactional Analysis, we can divide the mind into three primary ego states - Parent, Adult, and Child. Each ego state comprises a discrete set of thoughts, feelings, and behaviours directly linked to specific aspects of an individual's capabilities and experience:

- Parent Ego State : This ego state contains behaviours, thoughts, and feelings copied from parental figures or authority figures. It can be nurturing and protective, or controlling and critical.
- Adult Ego State : The Adult is oriented towards current data and experiences, and functions autonomously and rationally. It evaluates and processes information and makes decisions based on available facts.
- Child Ego State : This ego state is the seat of emotion; it typically displays the same types of behaviours, thoughts, and feelings that were experienced during childhood.

The Parent, Adult and Child ego states are diagrammed as follows:

[Imagen: A black letter in a circle  Description automatically generated]

Note: There is no special significance in the ordering of ego states in the diagram.

## Cathexis

According to Transactional Analysis theory, when people "change mood", or change their mode of thinking and feeling, this may be because they have "moved" (or cathected) into a different ego state:

- The Parent : A person may display anger after "moving" into the Parent ego state.
- The Adult : A person may express rational thinking after "moving" into the Adult ego state.
- The Child : A person may express happiness after "moving" into the Child ego state.

So rather than saying that the person has changed their mood, TA suggests that the person has emotionally engaged a different area of their psyche (i.e. a different ego state), which subsequently displays its own typical behaviours.

For example, take a day in the life of a bank manager:

- Parent : In a team meeting, the manager moves into his Parent ego state, offering guidance and setting expectations with a tone of authority and experience.

- Adult : Later, as he analyses data and strategizes the bank's next steps, the manager moves into his Adult ego state. Here, he is rational, pragmatic, and focused on the here and now.

- Child : In the evening, while playing with his young child, the manager enters the Child ego state. Now he is spontaneous, playful, and emotionally expressive.

In Transactional Analysis terminology, moving into an ego state is called cathexis; the manager cathected into the Parent in the meeting, he cathected into the Adult when number crunching, and he cathected into the Child when playing with his own child at home.

## Favourite Ego States

From a simple TA perspective, we would understand that every person has three ego states, Parent, Adult and Child, which they access at will and as appropriate to the situation.

However, Transactional Analysis suggests that many people have a "favourite ego state". This means that a person may prefer to "spend most of their time" in a specific ego state. For example:

- A mathematician may prefer the Adult , since this is where they think logically.
- A teacher may prefer the Parent , because this is where they act in a parental manner towards their students.
- A comedian may prefer the Child , because this is where they are amusing and jolly.

Staying in the ego state most suited to their profession allows these professionals to hone their professional skills and to develop those parts of their personalities which they need for making a living.

Additionally, it is also possible that these different professionals initially chose their professional callings based on their preferred ego state.

- The mathematician knew he was good at analytical thinking, due to his predisposition for the Adult, and therefore chose maths.

- The teacher knew he was good at parenting style behaviour due to his predisposition for the Parent, and therefore chose teaching.

- The comedian knew he was good at entertainment due to his predisposition for the Child, and therefore chose the entertainment industry.

In this way, the tendency people have towards a particular ego states can determine their careers, as well as being part of that which moulds their essential personalities.

The teacher, by ChatGPT

The mathematician, by ChatGPT

The comedian, by ChatGPT

---

# Chapter 25. Transactional Analysis (proper)

| Transactional Analysis is called Transactional Analysis because it started off as a way of analysing the social transactions that occur between different people. In other words, whereas other schools of psychoanalysis concentrated more on the internal processes that occur within the mind, Transactional Analysis suggested that if we can understand the actual meaning of interpersonal dialogue (rather than the obvious meaning), then we are well on the way to addressing the behavioural and emotional issues that plague people from time to time. |
|---|

Transactional Analysis views social interactions as transactions between discrete and well-defined ego-states. It analyses the ego states involved in these exchanges to understand communication patterns and relationship dynamics.

Transactional Analysis (proper) can be complex and involved, the following are some of the basic transaction types identified by TA.

## Complementary Transactions

Complementary transactions occur when the first person communicates from one specific ego state and the other person responds appropriately from the corresponding, complementary ego state.

---

For example:

Adult to Adult Transaction: Logical, factual communication between two people speaking as rational adults.

[Imagen: A diagram of a traffic light  Description automatically generated]

Child to Child Transaction: Appropriate and predictable emotional interaction between two people.

[Imagen: A traffic light with text below  Description automatically generated with medium confidence]

---

Child to Parent Transaction: A child-like expression of need or emotion which elicits a nurturing parent-like response.

[Imagen: A traffic light with black lines  Description automatically generated with medium confidence]

These transactions are considered complementary because they are predictable and effective, facilitating clear communication.

When transactions are complementary, the communication can continue indefinitely. Problems arise in communication when transactions are crossed (see next section), leading to misunderstandings, conflicts, and breakdowns in communication.

Checking the time, by ChatGPT

---

## Crossed Transactions

Crossed transactions in Transactional Analysis occur when an individual responds to a communication from an unexpected ego state, leading to a breakdown in communication.

Unlike complementary transactions, where responses match the ego state from which the initial message was sent, crossed transactions involve mismatched responses, which results in confusion, conflict, or miscommunication.

Example

Imagine a conversation between Alex and Jordan. Alex is speaking from the Adult ego state, and Jordan is responding from the Child ego state.

Alex (Adult): "Could you please update the report by tomorrow? We need it for the meeting."

Jordan (Child): "What's your problem exactly? Everyone else around here gets more time!"

From a TA perspective, this communication breakdown can be modelled as a crossed transaction:

Alex addresses Jordan's Adult, from his Adult. Jordan responds from an ego state that was never addressed, the Child, to Alex's Parent, which never spoke to him.

This is because Jordan perceived Alex's rational request as being critical or demanding, and so responded with a defensive, emotional reaction typical of the Child.

Such a transaction is called a crossed transaction because, diagrammatically, the lines of communication cross each other. (However, it is worthwhile noting that crossed transactions can also occur where this does not occur.)

This mismatch can lead to conflict or a breakdown in communication, as the two individuals are effectively 'talking past' each other, engaging in different types of dialogue.

From a psychotherapeutic perspective, resolving miscommunication that arises from crossed transactions involves recognizing the ego states at play and adjusting the responses to become complementary, thereby re-establishing effective communication.

The Misunderstanding, by ChatGPT

## Dual Level Transactions

Transactional Analysis identifies two types of dual transactions: ulterior transactions and angular transactions.

Both ulterior transactions and angular transactions include two levels of communication, however they differ in the way these levels are used in combination:

- Ulterior Transactions : Here communication happens at two levels, both of which are acknowledged and understood by all parties involved.

- Angular Transactions : In this case, the two levels of communication have different, possibly contradictory, purposes. The angular transaction represents an ulterior motive of the conversation initiator, of which the other person is unaware.

If the recipient responds to the unstated, covert intention of the initiator, then this is called a successful Angular Transaction; the initiator has "hooked" the recipient. On the other hand, if the recipient of the transaction responds to the stated, overt intention of the initiator, then the Angular Transaction was unsuccessful.

### Ulterior Transactions

An ulterior transaction in TA involves two messages being sent simultaneously: an overt, social message and a covert, psychological message. The social, overt message is what is openly said or expressed, while the covert, psychological message is hidden or implied. Both the initiator and recipient are fully aware of both levels of communication, however.

We can identify two types of Ulterior Transaction: Positive Ulterior Transactions and Negative Ulterior Transactions.

---

Positive Ulterior Transactions

An example of a positive ulterior transaction could occur where someone encourages a friend; in this case the covert message can be used to convey empathy or understanding.

Overt Message: "You're always so calm under pressure."

Covert Message: This might be a subtle way of encouraging a friend who is going through a tough time, without directly addressing their struggles. The friend understands the deeper meaning and feels supported.

[Imagen: A diagram of a traffic light  Description automatically generated]

In this example, the interactions involve a combination of the Nurturing Parent, Adult, and Child ego states. The initiator's Adult states a fact, their Nurturing Parent provides support and affirmation and the recipient's Child responds to the validation undercurrent.

---

Negative Ulterior Transactions

Negative ulterior transactions can carry a superficially benign or neutral overt message but have a covert, potentially harmful psychological message. These transactions can be damaging because they involve subliminal aggression.

For example:

Overt Message: "Wow, you got your last project done on time? That's amazing!"

CovertMessage: This message subtly implies that it is unusual or unexpected for the person to achieve success, indirectly suggesting incompetence or unreliability.

[Imagen: A diagram of a project manager  Description automatically generated]

In this example, the interactions involve a combination of the Critical Parent, Adult, and Child ego states. The initiator's Adult states a fact, their Critical Parent denies the validity of the recipient and the recipient's Child may respond to the disparaging undercurrent by feeling hurt and unvalued.

### Angular Transactions

Angular transactions in Transactional Analysis refer to a type of communication where an individual sends a message to another person on an overt social level, but there is a hidden psychological message that is directed to a different part of the recipient's personality.

Angular transactions often occur when a person has a hidden agenda or motive; the sender might be trying to manipulate or control the recipient in a subtle way. If the receiver responds to the hidden psychological message rather than to the overt social message, then the angular transaction is said to be successful.

The following diagram shows a successful angular transaction.

Ostensibly, the salesperson is simply telling facts to the customer. There is however an angular transaction from the salesperson's Adult to the customer's Child which effectively says, "Make sure you don't miss out on this limited opportunity!"

In this case, the salesperson gets the sought-for response from the customer's child and makes a sale.

---

# Chapter 26. Second Order TA Structural Analysis

## Sub-Ego-States

The high-level psychoanalytic model suggested by Transactional Analysis is simple and consists of three ego states: Parent, Adult and Child. Human behaviour is far more complex than this simple model suggests, however.

One way in which Transactional Analysis theory refines the three ego-state model is by introducing second-order ego-states (or, sub ego-states).

This means to say as follows; just as the whole psyche is understood to consist of three ego-states, so too each ego-state is understood to consist of a further three sub ego-states. (Transactional Analysis theory further suggests that each sub ego-state can be further subdivided into sub-sub-ego-states, and so on, to a very fine level of granularity.)

This subdivision can be diagrammatically represented as follows.

[Imagen: A diagram of a diagram of a parent and child  Description automatically generated]

Practically speaking, this means that each ego state (or, state of mind) has its own:

- Centre of control : The sub-parent ego state.

- Centre of reasoning : The sub-adult ego state.

- Centre of emotion : The sub-child ego state.

In this way, each ego state has its own internal "life" and can function independently of the rest of the psyche.

The following detailed list explains how we may imagine the identity and nature of each of the second-level sub ego states:

### Child Sub-Ego-States

- Parent in the Child: A child displays parental behaviour, but in a childlike manner.

- Adult in the Child: A child displays rational thinking, but in an uninitiated childlike manner. Eric Berne refers to the Adult in the Child as "the Little Professor," it's like a child playing at being an academic.

- Child in the Child: The child's pristine wonder and emotion.

### Parent Sub-Ego-States

- Adult in the Parent: The Adult in the Parent may occur when a parent assists their child by being rational.

- Child in the Parent: The Child in the Parent may occur when a parent supports their child in an emotional manner.

- Parent in the Parent: The Parent in the Parent may occur when a parent seeks to modify their child's behaviour by asserting their parental rights.

### Adult Sub-Ego-States

- Parent in the Adult : This sub ego-state can emerge when an individual in their Adult state adopts a guiding or nurturing role, reminiscent of a Parental figure. It's an ego state where Adult logic and understanding are used to provide support or correction in a parental style.

- Child in the Adult : Here, the Adult ego state is influenced by the characteristics of the Child. This could manifest as creativity, spontaneity, or emotional expression within a framework of adult reasoning and responsibility.

- Adult in the Adult : This is the purest form of the Adult ego state, characterised by rational thinking, problem-solving, and mature interactions with the world. It represents the Adult ego state functioning independently, without significant influence from the Parent or Child sub-states.

Each sub ego-state offers a subtly different mode of behaviour and thinking, which allows for a more nuanced appreciation of the dynamics at play in human interactions and intrapersonal processes.

Parent in the Child. Creator: Unsplash

---

# Chapter 27. Intra-Psyche Communication Channels

The second-level TA structural analysis of the psyche allows us to refine the intra-psyche model of communication, as per the following diagram:

## Channels of Communication

Elaborating on the internal channels of communication represented in the above diagram provides the following analysis:

### Interactions Among Sub-Ego-States within the Adult

The Adult in the Adult Communicates with:

- Parent in the Adult : This communication represents the rational, problem-solving aspects of the Adult ego state engaging with the nurturing, guiding elements of the Parent sub-state within the Adult. This is where logical thinking meets parental wisdom and guidance.

- Child in the Adult : Here, the Adult in the Adult, characterised by rationality and maturity, communicates with the mature Child aspect of the Adult.

### Interactions between the Adult Sub-Ego-States and the Parent and Child

The Parent in the Adult Communicates with:

- Adult in the Parent : This interaction represents the guidance and nurturing aspects of the Parent within the Adult ego state engaging with the rational, responsible elements of the Adult sub-state within the Parent. This is a blend of parental guidance with adult reasoning and responsibility.

The Child in the Adult Communicates with:

- Adult in the Child : This reflects the emotional, creative, and spontaneous aspects of the mature Child within the Adult ego state communicating with the rational, thoughtful aspects of the Adult within the Child ego state. This is where the inner child's creativity and emotions are tempered by adult-like thoughtfulness and reasoning.

---

### Interactions Among Sub-Ego-States within the Parent and the Child

The Adult in the Parent Communicates with:

- Parent in the Parent : This interaction represents the rational and responsible elements of the Adult within the Parent ego state communicating with the authoritative and guiding aspects of the Parent within the Parent. This is where parental logic meets parental authority and guidance.

- Child in the Parent : In this communication, the Adult within the Parent engages with the emotional, childlike aspects of the Child within the Parent. This reflects a softening of the Parent's parental stance and may also invoke emotional support for a child.

The Adult in the Child Communicates with:

- Child in the Child : Here, the rational, thoughtful aspects of the Adult within the Child ego state communicate with the pure, emotional, and spontaneous aspects of the Child within the Child. This is a blend of childlike wonder and innocence with child-like thoughtfulness and understanding.

- Parent in the Child : This represents the interaction between the Child's rationality and the Child's ability to be nurturing and guiding.

These interactions demonstrate the complex and dynamic nature of internal communication within an individual's psyche according to TA.

The model presented underscores the multifaceted nature of our internal experiences, where different aspects of self (Parent, Adult, Child) and their sub-states engage in a continual dialogue, shaping our behaviour and internal processes.

---

# Section V - Psychoanalysis using AI

This section illustrates the psychoanalytical capabilities of an advanced generative AI model like Chat GPT 4.

So how are you feeling today?, by ChatGPT

---

# Chapter 28. Performing Structural Analysis using ChatGPT

## Structure of the Psyche

As explained in the previous section, TA Structural Analysis identifies the internal ego-state structure unique to each individual.

This means that although each individual is born with a full complement of ego states: Parent, Adult and Child, nevertheless people develop particular habits about which part of their psyche they decide to "hang around in" and fine tune. Some people may prefer to interact from the Parent (e.g. a teacher), some from the Adult (e.g. a mathematician), and some from the Child (e.g. a comedian).

Understanding the preferred ego states of other people and of ourselves can help us optimise our personal interactions and to know "what will work and what won't work" from a social perspective.

## Psychoanalysing the Beatles

ChatGPT is impressively good at performing Structural Analysis and identifying preferred ego states, as the following example demonstrates. (This example uses a GPT designed for this purpose, Ego State Behaviour Analyser - https://t.ly/9LDfx.)

| You Analyse which ego state was favoured by each member of the Beatles and how this affected the band's dynamic. Ego State Behaviour Analyser To analyse the favoured ego states of each member of the Beatles and how these influenced the band's dynamics, we need to look at their behaviours, public personas, and interactions, both as individuals and as a group . The Transactional Analysis (TA) framework categorises ego states into three primary categories: Parent, Adult, and Child. These states are not literal age-related categories but rather represent styles of thinking, feeling, and behaviour. John Lennon : Lennon often exhibited characteristics of the Child ego state , especially in his early years with the Beatles. His playful and rebellious nature, tendency for emotional and creative expressions, and his advocacy for peace and love align with the Free Child sub-state. However, Lennon also showed aspects of the Critical Parent, particularly in his later years, where he was more outspoken about social issues, displaying a tendency to critique and challenge societal norms. Paul McCartney : McCartney generally favoured the Adult ego state , characterised by his rational, organised approach to music production and business matters. His ability to balance creativity with practicality and his often-mediating role in the group suggest a strong Adult presence. Additionally, McCartney displayed nurturing aspects of the Nurturing Parent state, particularly in his care and concern for the group’s wellbeing and harmony. George Harrison : Harrison's behaviour leaned towards the Adult ego state , especially evident in his spiritual and philosophical interests. He approached life and music with a reflective and introspective manner, often seeking deeper meaning and understanding. His immersion in Eastern spirituality also indicates a tendency towards the Adapted Child state, reflecting a desire for inner peace and acceptance. Ringo Starr : Starr often demonstrated characteristics of the Adapted Child ego state , displaying compliance and a willingness to go along with the group's decisions. His good-natured and easy-going demeanour, coupled with a somewhat less dominant role in the group's decision-making, aligns with this state. However, Starr also showed elements of the Adult state, particularly in his steady and reliable presence within the band. Impact on Band Dynamics : The interplay of Lennon's Child and Parent states with McCartney's predominantly Adult state likely created a dynamic tension in the band, driving creativity but also leading to conflicts. Harrison's Adult state, coupled with his Adapted Child tendencies, may have positioned him as a more introspective and stabilising force within the group, though possibly leading to feelings of being overshadowed by the more dominant personalities of Lennon and McCartney. Starr’s Adapted Child state provided a flexible and accommodating presence, which may have helped in balancing the stronger ego states present in the band. This analysis is a broad and generalised interpretation based on public personas and known behaviours. It's important to note that individuals can shift between different ego states depending on the context, and a more nuanced analysis would require a deeper exploration of their personal histories and private lives. |
|---|

Impressively, in addition to identifying the primary ego states which the different singers tended to be "in", ChatGPT also provided a compelling explanation of the interaction between the group members in terms of their "favourite" ego states.

This psychoanalytical capability of ChatGPT could be useful for determining which ego states people in a real-life situation are "in" and choosing an effective course of action correspondingly.

The Beatles 1964 concert, Wikimedia Commons

---

## Practical Applications of AI Structural Analysis

The practical applications of ChatGPT's ability to perform TA Structural Analysis are virtually unlimited. This ability can theoretically be used in any case where we want to optimise the interactions between computers and people, or the interactions between people and people.

Some examples of where this AI capability can be applied are:

- Leadership and Management : Leaders and managers can use ChatGPT's structural analysis to understand the dominant ego states within their teams. By recognizing whether team members operate from the Parent, Adult, or Child states, leaders can tailor their communication and management strategies to motivate their teams, resolve conflicts, and enhance teamwork.

- Enhancing Therapeutic Practices : Therapists and counsellors can use ChatGPT to aid in the identification of clients' ego states, streamlining the diagnostic phase and enriching therapy sessions.

- Improving Educational Outcomes : Educators can use ChatGPT to understand the ego states of their students, thus adapting teaching methods to better engage them. Understanding whether a student is operating from a Child, Adult, or Parent state can help in tailoring lesson plans and interactions to encourage more effective learning.

- Optimising Marketing and Customer Service : Marketing professionals and customer service representatives can benefit from understanding the ego states of their audience or customers to craft messages that resonate with the target ego state, improving communication effectiveness and customer satisfaction.

By understanding "people are coming from" we can customise computer-human interactions and person-person interactions to customise and optimise the experience, leading to more effective, efficient, and satisfying outcomes for all parties involved.

---

# Chapter 29. Performing Transactional Analysis (proper) using ChatGPT

In addition to its capabilities in Structural Analysis, ChatGPT is capable of doing an accurate Transactional Analysis (proper) of social interactions and conversations; the following example uses a GPT designed for this purpose (Transactional Analyst GPT -https://t.ly/N1SYj).

| You Analyse : Manager : "Hey, I know you're swamped, but did you manage to finalise that report? The executive team's expecting it tomorrow, and I need to review and add my input before then. It's crucial for our department's funding proposal." Worker : "Why must you keep pressing me about it? I'm already juggling a dozen other tasks. I assured you, it'll be completed. Trust me to handle my responsibilities!" Manager : "I understand, but this report is a top priority. Our department's future projects hinge on it. I need you to prioritise this above all else today. And, let's try to maintain a professional tone, shall we?" Worker : (sighs, rubbing temples) "Fine, I'll reshuffle my schedule and push some tasks to tomorrow. But understand this puts a strain on my other deliverables. I'll have the report on your desk by the end of the day, but at a cost to other projects." Manager : "I appreciate your effort. Let's sit down after you're done and discuss how we can better manage the workload going forward. I'm here to support, not just to push for deadlines. " Worker : (nods reluctantly) "Alright, let's focus on getting this done first. We'll talk later." Transactional Analyst In this conversation, we can observe different ego states from Transactional Analysis theory in action. Manager's Ego States : Parent Ego State: The manager initially speaks from a 'Parent' ego state, expressing concern and authority about the report and its importance. This is evident in the manager's directive language, like "I need to review" and emphasising the report's significance for funding. Adult Ego State: When the worker expresses frustration, the manager shifts to an 'Adult' ego state, trying to reason with statements like "this report is a top priority" and offering future support. This is a rational, problem-solving approach. Worker's Ego States : Child Ego State: The worker initially responds from a 'Child' ego state, evident in the emotional and defensive reaction ("Why must you keep pressing me about it?"). This state often surfaces in response to feeling pressured or misunderstood. Adult Ego State: Later, the worker moves towards an 'Adult' ego state, acknowledging the situation's reality ("Fine, I'll reshuffle my schedule") and agreeing to discuss the workload later. This shift demonstrates a more practical and solution-focused approach. Transactional Analysis : Crossed Transactions: Initially, there is a 'crossed transaction' where the manager's 'Parent' state addresses the worker's 'Adult' state, but the worker responds from the 'Child' state. This mismatch creates tension and conflict. Complementary Transactions: Later, the conversation shifts to 'complementary transactions' with both parties operating from their 'Adult' states, leading to a more constructive and problem-solving dialogue. Overall, the conversation demonstrates how shifts in ego states can influence the dynamics of a transaction. Initially, the conversation is strained due to mismatched ego states, but it becomes more productive as both parties shift to their 'Adult' states, focusing on practical solutions and mutual understanding. |
|---|

In this case, ChatGPT accurately identifies an initial crossed transaction which then moves into a complementary transaction, leading to a positive outcome.

## Analysing Spam Email using Transactional Analysis (proper)

Spam email with a social engineering exploit typically consists of an ulterior transaction designed to "hook" the Child ego state of the recipient.

The following typical SPAM email presents too-good-to-be-true information to the user in the hope of bypassing the recipient's Adult ego state and hooking their Child into providing their credit card details to the sender.

| From: ExcitingOpportunities@wonderlandpromo.com To: [Recipient's Email] Subject: � � Unlock Your Dreams! A Once-in-a-Lifetime Surprise Awaits You! 🌟 Dear [Recipient's Name], � � Congratulations! � � You've been specially selected for an unbelievable adventure that we guarantee you've never experienced before! Remember those dreams you had where anything seemed possible? It's time to make them come true ! We at Wonderland Promotions believe in the magic of dreams and the spirit of endless possibilities. That's why we've handpicked YOU for a surprise so big, you'll be talking about it for years! 🚀 But here's the catch - this is a secret, limited-time offer, just for you. Why? Because we know you're someone who still cherishes the wonders of the world and you're not afraid to take a leap of faith into the extraordinary. What do you need to do? It's simple! Just click the link below, enter your personal details (don't forget your credit card info for a small processing fee), and the journey to your dream adventure begins! [Exciting Link to Wonderland] Don't let this chance slip away! After all, what's life without a little adventure? Act fast, as this offer disappears in 48 hours! Can't wait to see you on the other side, where dreams become reality! � � Best Wishes, Alice Adventure Wonderland Promotions P.S. Remember, great opportunities don't come knocking twice! 😉 |
|---|

Using the same GPT as above (Transactional Analyst GPT - https://t.ly/N1SYj), let's see what ChatGPT makes of this email.

| You Analyse : (email text…) Transactional Analyst In the context of Transactional Analysis, the email from ExcitingOpportunities@wonderlandpromo.com can be analysed as an angular transaction. In angular transactions, the communication involves a hidden agenda or motive that is not explicitly stated in the social message. Here's how this applies to the email: Apparent Social Message (Surface Level) : On the surface, the email is framed as an enthu siastic and enticing invitation. It uses emotive language and promises a unique, exciting adventure. This part of the message is designed to appeal to the recipient's Child ego state, which is more open to excitement, novelty, and adventure. Hidden Psychological Message (Underlying Intent) : The underlying motive of the email is not as overt. The sender appears to have a hidden agenda, which is to persuade the recipient to click on a link and enter personal and credit card information. This action is subtly encouraged under the guise of a limited-time, exclusive offer, tapping into the recipient's sense of urgency and fear of missing out. Dynamics of the Angular Transaction : Sender's Ego States : The sender is operating from a Controlling Parent ego state, as they are attempting to manipulate the recipient's behaviour through persuasive language and creating a sense of urgency and exclusivity. Targeted Ego State of the Recipient : The message is directed towards the recipient's Child ego state, seeking to evoke an impulsive, emotional response. The aim is to bypass the recipient's Adult ego state, which would normally analyse the situation more critically and logically. Outcome of the Angular Transaction : The success of such an angular transaction depends on whether the recipient responds to the overt, social message or recognizes the covert, psychological intent. If the recipient responds positively to the social message (e.g., by clicking the link and providing information), the sender's hidden objective is achieved. However, if the recipient's Adult ego state intervenes and questions the legitimacy or motives behind the email, the angular nature of the transaction is exposed, and the sender's hidden agenda may not succeed. In summary, the angular nature of this transaction lies in the discrepancy between the overt enthusiasm and promise of an exciting opportunity (social message) and the covert intent to obtain personal and financial information (psychological message). The effectiveness of such a transaction depends on the recipient's ability to discern and respond to these two levels of communication . |
|---|

That was pretty obvious. Let's try a slightly trickier phishing email on the Transactional Analyst GPT.

Shared Chat: https://t.ly/Ql2y_

| You Analyse this email: " Hello, We have received several reports against your activity! You have posted many videos that violate our rules. Reports claimed that your posts violated Facebook Policies regarding third party intellectual property rights. Based on our policies, robotic growth of followers , sensitive content, human rights violators, animal rights violators or even copyrights should be prohibited. Referring to reports on your page, your page has been set up in the deletion process. Please first look at the activity on your site and if you think this is a mistake , please contact us. For appeal and for more details below at the link. https://www.facebook.com/4238954357356/ Appeals after 48 hours wont be taken into consideration Sincerely, Facebook Team " Transactional Analyst The email presents a transaction that appears to be an angular transaction, carrying both overt and covert messages aimed at eliciting a specific reaction from the recipient . Here's an analysis based on the provided content: Overt Transaction Adult-Adult Ego State : The overt content of the email claims to address a serious concern regarding violations of Facebook's policies. It purports to inform the recipient about alleged activities such as posting videos that violate rules, engaging in prohibited behaviours like robotic growth of followers, and other infringements related to intellectual, animal, and human rights. The message concludes by offering an option to appeal the decision within a specific timeframe, ostensibly respecting the recipient's ability to rectify the situation. Covert Transaction Child-Parent Ego State : The covert message, designed to "hook" the recipient's Child ego state, aims to create anxiety and urgency. The mention of "several reports against your activity" and the setup of the page "in the deletion process" are likely to provoke fear and prompt immediate action without critical thinking. This urgency is compounded by the deadline for appeals, pushing the recipient to act hastily. Angular Aspect : The link provided for the appeal is the most critical part of the angular transaction. Although it seems to offer a solution, its real purpose could be to deceive. By urging the recipient to click a potentially malicious link, the sender may be aiming to compromise personal information or security. This part of the message targets the recipient's anxiety and fear, exploiting their emotional state to trigger an impulsive response. Tactics Used: Urgency and Fear : Creating a sense of urgency to prompt immediate action, bypassing rational analysis. Authority Claim : Posing as the "Facebook Team" to add legitimacy to the demand. Threat of Loss : Suggesting that the recipient's page is already in the process of deletion to instigate a fear of losing something valuable. Conclusion This email likely constitutes a phishing attempt, exploiting psychological manipulation to deceive the recipient into clicking a malicious link under the guise of resolving a policy violation issue. The transaction is designed to bypass rational analysis (Adult ego state) and directly appeal to emotional responses (Child ego state), specifically fear and urgency, to trick the recipient into compromising their security or personal information. |
|---|

ChatGPT correctly identifies the typical hidden agenda of the spammer and identifies the angular transaction with which the spammer is trying to hook the Child ego state of the recipient.

Practically speaking, this AI ability could be used in an email service to mark spam those emails that constitute angular transactions.

Too good to be true, by ChatGPT

---

## Real Time Transactional Analysis

Consider the following unsuccessful conversation between a sales representative from an energy retail company and a customer who is about to leave the company.

| Sales Rep: Good afternoon! May I speak with John, please? Customer: This is John. What's this about? Sales Rep: Hi John, I'm Eddie from Blue Star Energy. We noticed you've requested to switch to a different electricity provider. Before you make a final decision, we'd really appreciate the opportunity to discuss your current plan and see if there's anything we can do to enhance your experience with us. Customer: I've already made up my mind. Your rates are too high, and I found a better deal elsewhere. Sales Rep: I completely understand that finding a good deal is important. However, we truly value your business and would hate to see you go. To show how much we appreciate you, we're prepared to offer you a $50 voucher if you decide to stay with us. This could be a great way to reduce your next bill significantly. What do you think? Customer: I'm not interested in vouchers. I'd prefer lower rates instead of one-off deals. Sales Rep: Of course, I can see where you're coming from. But consider this: the $50 voucher is as good as cash. You can use it towards your bill, effectively lowering your rates for the next billing cycle. Plus, we're constantly reviewing our plans to ensure they're competitive. There's a lot of value in staying with us, beyond just the numbers. Customer: I don't think you're getting it. It's not just about this next bill or a one-time voucher. I want consistently lower rates. Sales Rep: I understand your concern about consistent savings, John. Still, this voucher is a step in that direction. It's a quick win while we work on making our rates more competitive for you in the long run. And, you won't fin d the level of service we offer anywhere else. Why not give us another chance? Customer: You're not really listening to me. I've already told you what I need, and a one-off voucher isn't it. I'm looking for long-term savings, not short-term incentives. Sales Rep: But if you consider the overall benefits and services we provide, plus this voucher, you'll see that staying with us is the right choice. We're constantly improving our offerings, and we'd love to have you experience these enhancements first-hand. Customer: No, thank you. I think we're done here. [At this point, the customer becomes increasingly frustrated due to the sales rep's insistence on the voucher and perceived lack of understanding regarding the customer's request for consistent long-term savings rather than short-term incentives. The sales rep fails to read the customer's growing annoyance, continuing to push the voucher offer.] Customer: I've made my decision. Please, just process my switch request. Goodbye. [The customer hangs up, feeling unheard and dissatisfied with the sales rep's approach.] |
|---|

Let's run that conversation through the Transactional Analyst GPT (https://t.ly/N1SYj) to find at which stage the sales representative could have corrected his approach.

Shared Chat: https://t.ly/cF-jc

| You Identify where a crossed transaction occurred in this conversation and explain how the call could have been handled better. "Sales Rep: Good afternoon! May I speak with John, please...] " Transactional Analyst In this conversation, the crossed transaction occurs when the Sales Rep continues to offer the $50 voucher despite the Customer expressing a clear preference for consistently lower rates over one-off deals. The Sales Rep's persistent focus on the voucher and benefits of staying with the company does not align with the Customer's expressed need for long-term savings. This misalignment demonstrates a failure in the transactional communication, where the Sales Rep responds to the Customer's Adult ego state with messages aimed at appealing to the Child ego state by offering immediate gratification (the voucher), rather than addressing the Adult concern for long-term financial benefits. Better Handling of the Call: Acknowledgment and Empathy : The Sales Rep could have acknowledged the Customer's concern more effectively by showing empathy towards the Customer's situation. A response like, "I see that finding a solution that offers long-term savings is really important to you," would validate the Customer's feelings and concerns, aligning with the Customer's Adult ego state. Direct Address of Concerns : Instead of repeatedly offering the voucher, the Sales Rep could have explored or proposed alternative solutions that align with the Customer's request for lower rates. For example, the Sales Rep could have said, "Let's review your current usage and see if there's a more cost-effective plan that would offer you the lower rates you're looking for on a consistent basis." Offer to Follow-Up : If immediate alternatives were not available, the Sales Rep could have offered to follow up after discussing with their team or management to find a more suitable offer. This approach would demonstrate a commitment to genuinely addressing the Customer's needs. Respect the Customer's Decision : Recognizing and respecting the Customer's decision to switch providers is crucial. The Sales Rep could have ended the call on a positive note by saying, "I understand your decision. While we're sorry to see you go, I'll process your switch request right away. If anything changes or you'd like to discuss future options, please feel free to contact us." By focusing on genuinely understanding and addressing the Customer's needs, the Sales Rep could have avoided the crossed transaction and potentially maintained a positive relationship, even if the Customer ultimately decided to switch providers. This approach would leave the door open for future business and ensure the Customer felt heard and respected. |
|---|

The GPT is able to accurately identify at which stage a crossed transaction occurred, and what could have been done to avoid a negative outcome to the call.

In practice, an AI could monitor sales calls in real time and alert the sales rep when they were getting into a crossed transaction, so that  they could adjust their approach to better suit the ego state from which the customer was addressing  them.

Next call, by ChatGPT

---

# Section VI - Synthesizing the Human Mind

This section shows how we can combine Transactional Analysis theory together with generative AI to synthesize patterns of human thought.

In trouble again, by ChatGPT

---

# Chapter 30. Synthesising Ego States using AI

So far, we have shown how generative AI can use Transactional Analysis to analyse human interactions and understand human behaviour.

Let's see if we can also synthesise ego states or an entire human psyche by using Chain of Thought Prompting and Transactional Analysis.

## Synthesising Ego State Activity

At the simplest level, to simulate a TA-psyche using Chain of Thought Prompting, we must split the AI processing into the primary ego states, Parent, Adult and Child.

In other words, instead of using generative AI in a monolithic way, we can use Chain of Thought Prompting to simulate Parent, Adult and Child ego state processing and then recombine the output of these discrete synthetic ego states, as occurs in real life.

The following conversation occurred with a GPT called TA Chat (https://t.ly/IAM0b), which is configured to provide a response from Adult, Parent or Child ego states, as appropriate.

| You It's so dull in London today TA Chat Free Child : Oh, I can imagine that! Sometimes London can feel like it's wearing a big grey hat, can't it? But hey, even on dull days, there's always something fun or new to explore. Maybe it's a perfect day for a cosy cafe or a visit to one of those amazing museums! Nurturing Parent : I understand that grey days can be a bit gloomy. It's important to take care of yourself during these times. Perhaps you could use this opportunity to do something comforting, like reading a good book or having a w arm cup of tea. Remember, taking a moment for yourself can really brighten your day. Adult : While the weather is something we can't control, we can certainly find ways to make the most of it. If you're looking for indoor activities, London offers many. You could visit a gallery, explore a historical site, or enjoy some indoor sports or leisure activities. Or, it could be an opportunity to plan or organise something indoors, turning the day into a productive one. |
|---|

This output compares favourably with the following conversation with base ChatGPT.

| You It's so dull in London today ChatGPT I'm sorry to hear that it's a dull day in London. If you're looking for something to brighten your day, I can create a digital image for you. Just describe what you'd like to see, and I'll generate an image accordingly. Whether it's a sunny landscape, a colourful abstract piece, or anything else, feel free to let me know your preference! |
|---|

Because we asked ChatGPT to respond from each ego state discreetly, it is more informed and specific in the response from each ego state.

[Imagen: A group of people walking in Trafalgar Square  Description automatically generated]

A Rainy Day in London, Wikimedia Commons

## Choosing a Preferred Ego State Response

Now let's allow the user to choose which ego state response they liked best, this will allow the GPT to continue the conversation in the vein best suited to the user.

In the following conversation, the GPT has been updated to ask the user which ego state response they prefer, and then to continue the conversation from that ego state.

| You It's so dull in London today TA Chat Free Child : "Oh, a gloomy day in London? That's just a perfect excuse to have some indoor fun! Maybe it's time to explore a cosy cafe, dive into a good book, or start an exciting indoor adventure. Who says the rain has to spoil the day?" Nurturing Parent : "I understand that a dull day can feel a bit disheartening. It's important to remember that every day has its own beauty, even the grey ones. This might be a lovely opportunity to relax, take care of yourself, and enjoy some peaceful moments indoors. How about some tea and a comforting activity?" Adult : "Acknowledging that the weather in London can often be overcast, it's helpful to have a plan for these days. Indoor activities, whether they are productive tasks or leisure pursuits, can be quite fulfilling. You might consider visiting a museum, working on personal projects, or simply organising your space. It's all about making the most of the situation." Which perspective do you prefer - Free Child, Nurturing Parent, or Adult? You Chil d TA Chat Free Child : "Awesome choice! Let's turn this dull day into an exciting one! How about creating your own little indoor adventure? Maybe build a fort with blankets, have a movie marathon with your favourite snacks, or even start a new hobby that's been on your mind. The day is yours to make fun, no matter the weather. Let's make the most of it with a smile and a dash of creativity!" 🌟🎉 Ready to make today unforgettable? What's your first fun activity going to be? 🚀🌈 |
|---|

Or:

| You I need a boost in my IT career TA Chat Free Child: Hey there! You're looking for a career boost in IT? That's awesome! Dive into the latest tech trends, like AI or cybersecurity. Have you thought about creating a cool app or joining some fun hackathons? Networking with other tech enthusiasts can be super exciting too. Remember, learning new skills and having fun with them is key! 🚀 Nurturing Parent: It's wonderful to hear you're seeking growth in your IT career. It's important to approach this with patience and kindness to yourself. Maybe consider enhancing your skills through online courses or certifications in areas you're passionate about. Don't forget the value of mentorship and networking. Remember, your well-being and work-life balance are just as important as professional development. 🌟 Adult: Advancing in your IT career involves a strategic approach. Assess your current skills and identify areas for growth. Certifications in high-demand fields like cloud computing or data analytics can be valuable. Also, consider developing your soft skills, such as communication and leadership, as they're essential in the IT industry. Networking and staying u pdated with industry trends is crucial. Set clear, achievable goals and actively work towards them. 📈 Which response resonates more with you - Free Child, Nurturing Parent, or Adult? I'll continue from that perspective to better assist you. You It seems like both the Child and Adult are making good points? TA Chat Free Child & Adult Blend: Fantastic! Let's combine the excitement and innovation from the Free Child with the strategic planning of the Adult. How about diving into the latest IT trends with enthusiasm and curiosity? You can explore areas like AI, blockchain, or whatever piques your interest. Joining hackathons or tech meetups can be a thrilling way to learn and network. At the same time, consider mapping out a career path. Maybe look into certifications or specialised training in areas that are booming. Balancing this adventurous spirit with focused career planning can create a dynamic and fulfilling journey in IT. Keep the passion alive while building a solid skillset. Ready to take this exciting and strategic leap? 🌌📊 |
|---|

This compares favourably with plain ChatGPT's response to the same input, which is waffly and mentions certifications that no longer exist or are outmoded.

| You I need a boost in my IT career ChatGPT Improving your career in IT can be a multi-faceted process, involving the development of both technical and soft skills. Here are some strategies to consider: Stay Updated with Technology Trends : IT is a rapidly evolving field. Keeping abreast of the latest technologies, programming languages, and methodologies is crucial. Consider following tech blogs, attending webin ars, and participating in online forums. Gain Certifications : Certifications can validate your skills and knowledge in specific areas. Depending on your field of interest, consider certifications like CompTIA, Cisco (CCNA/CCNP), Microsoft (MCSE/MCSA), AWS, or Google Cloud. Learn New Skills : Based on market demands and your areas of interest, learn new skills. For example, if you're in software development, learning about cloud technologies, AI, or data science could be beneficial. Networking : Build a professional network through platforms like LinkedIn, attend industry conferences, and join local tech groups or meetups. Networking can lead to new opportunities and insights into industry trends. Work on Projects : Hands-on experience is invaluable. Work on personal or open-source projects, or seek opportunities within your current job to work on different projects. This can also help in building a strong portfolio. Soft Skills Development : Communication, teamwork, problem-solving, and adaptability are key in IT. These skills can significantly impact your career progression. Mentorship : Find a mentor who can provide guidance, career advice, and help you navigate challenges in the industry. Higher Education : Depending on your career goals, pursuing a higher degree like a Master's in a specialised IT field can open up advanced career opportunities. Job Rotation or Internal Opportunities : If possible, explore different roles within your current organisation. This can broaden your experience and expose you to new challenges . Stay Motivated and Set Goals : Regularly set career goals, assess your progress, and stay motivated. Celebrate your achievements, no matter how small they may seem. Remember, career growth in IT isn't just about technical prowess; it's also about understanding the industry, being adaptable, and continuously seeking opportunities to learn and grow. |
|---|

The above example shows how by synthesising Adult, Parent and Child ego states, we can create a rich, interactive user experience and allow the user to communicate with the generative AI in the way that suits them, instead of being bound to the AI's base personality.

| Note : In reality, the above approach could be adopted without explicitly referring to ego states, the user could simply be asked which response they prefer. |
|---|

## Conclusion

Combining Transactional Analysis theory with Chain of Thought Prompting is a powerful tool that has significant potential in various fields, for example:

- Human-Computer Interaction : In human-computer interaction, the AI can enhance user experience by identifying the user's ego state and adjusting its interaction style.

For example, if a user is frustrated (Child state) with a service, the AI could adopt a Parent state, offering guidance and assistance. In scenarios where users are seeking information (Adult state), the AI can respond with clear, concise, and factual data, by maintaining an Adult-to-Adult communication style.

- Education and Personal Development : In education, AI can identify the ego state of students to tailor its teaching approach.

For a student in a Child ego state, showing curiosity and creativity, the AI can offer stimulating and engaging content. If a student is in an Adult state, seeking factual information, the AI can provide structured, detailed educational material. This personalised approach can enhance the learning experience and foster personal development.

- Business and Management : In business and management, AI can assist in understanding employee dynamics and improving team interactions. By analysing communication patterns, the AI can identify the dominant ego states within a team and advise managers on how to approach different members.

Across these diverse fields, the application of AI combined with manual or automatic TA-based CoT Prompting, has the potential to revolutionise interactions and services. By tailoring responses to the identified ego state of the user, AI can provide more effective, empathetic, and personalised support.

This advancement can not only enhance the efficiency of services across sectors but can also significantly improve the quality of human-AI interactions.

An argument with the lift, by ChatGPT

---

# Chapter 31. Consulting with Yourself using CoT Prompting

| This chapter is based on the Second Level Transactional Analysis theory presented in Chapter 27. Intra-Psyche Communication Channels. |
|---|

From an ideal Transactional Analysis perspective, when a person is presented with a quandary, the issue first "hits" the Adult.

The Adult then farms out the quandary to the Child and the Parent, each of which consider the question at hand from their own perspectives. Subsequently the Adult considers the "opinions" of the Child and the Adult and synthesizes a conclusion based on the feedback from all parts of the psyche.

In this way a person can make a decision that considers how that decision will impact on every part of the person's being and emotions.

## Simulating Internal Thought

We can simulate this thinking process flow using CoT Prompting (implemented in Python), by using the following algorithm:

- Receive the initial question.

- Translate the question to a Child-version of the question.

- Translate the question to a Parent-version of the question.

- Pass the Child-version of the question to the Child.

- Pass the Parent-version of the question to the Parent.

- Allow the Parent and the Child to determine their own answers.

- Let the Parent and the Child pass their individual answers back to the Adult.

- Let the Adult take the answers of the Parent and the Child into account, while formulating its own final conclusion.

By using this technique, we can explore the full gamut of options that would be considered by all aspects of the persona, and then take these options into account when forming a final, reasoned opinion.

Using the Python code from github.com/edwardchalk/SimulatingThought, let's see how this works in action.

## Walking The Lairig Ghru

In case you were wondering, the Lairig Ghru (pronounced Larry Grew) is a famous hill-walk in Scotland, it can also be hazardous and dangerous. Let's ask ChatGPT to simulate the internal thought process that may result from the following question:

| Initial question : Should I walk the Lairig Ghru today? The weather is wild and windy but the walk could be fun, and I feel fit and trim. |
|---|

First, ChatGPT generates the Parent and Child versions of the question:

| Parent ego state version of the question : Should I undertake the Lairig Ghru walk even though the weather conditions are harsh and windy, but I am physically prepared and in good shape? Child ego state version of the question : Should I take the adventurous risk and embrace the challenging weather conditions to walk in Lairig Ghru today despite feeling energetic and physically prepared for it? |
|---|

Subsequently, these questions then ricochet round the psyche as follows (if you don't want to read through the entire internal discussion, skip to the next section):

| Parent.Parent Absolutely not! Under no circumstances should you undertake the Lairig Ghru walk in harsh and windy weather conditions. It doesn’t matter if you are physically prepared and in good shape; safety should always be the top priority. Harsh weather conditions increase the risks of accidents and exposure, and it is your responsibility to prioritize your own well-being. As a strict disciplinarian, I must emphasize that no amount of physical fitness can guarantee your safety in extreme weather. Instead, wait for more favourable conditions and plan your walk accordingly. Parent.Child While you may be physically prepared and in good shape, undertaking the Lairig Ghru walk in harsh and windy weather conditions can be risky. It’s essential to consider the potential dangers and assess whether the conditions pose a significant threat to your safety. If the weather conditions are extreme or unpredictable, it’s advisable to postpone your trek for a more suitable time. If you’re determined to proceed, make sure to take necessary precautions and heed any advice or warnings from experienced local hikers or authorities. Additionally, ensure you have proper equipment, such as appropriate clothing, sturdy footwear, and navigation tools. Remember, personal safety should always be the top priority. If the weather conditions are severe or if you have any doubts about your safety, it’s best to err on the side of caution and choose a different activity or wait for better weather conditions. Parent.Adult Based on the answers provided, it is clear that safety should be the top priority when considering whether or not to undertake the Lairig Ghru walk in harsh and windy weather conditions. While being physically prepared and in good shape is important, it does not guarantee safety in extreme weather. I would advise to carefully assess the potential dangers associated with the current weather conditions. If the conditions are extreme or unpredictable, it would be wise to postpone the walk for a more suitable time. It is crucial to prioritize personal safety and not underestimate the risks posed by harsh and windy weather . If you still decide to proceed, taking necessary precautions is essential. Seek advice from experienced local hikers or authorities, as they may provide valuable insights and information about the conditions on the trail. Ensure that you have the appropriate equipment, including suitable clothing, sturdy footwear, and navigation tools, to handle the challenging conditions. Ultimately, it is crucial to make a well-informed decision and exercise caution when it comes to undertaking outdoor activities in severe weather. Understanding the potential risks involved and taking necessary precautions will help ensure a safe and enjoyable experience. Adult.Parent Based on the answer provided, it is evident that safety should be the primary consideration when contemplating whether or not to walk the Lairig Ghru in wild and windy weather conditions. While feeling fit and trim is important, it does not guarantee safety in extreme weather. I would advise carefully evaluating the potential hazards associated with the current weather conditions. If the conditions are severe or unpredictable, it would be prudent to postpone the walk for a more suitable time. It is paramount to prioritize personal safety and not underestimate the risks posed by harsh and windy weather. If you still decide to proceed, it is crucial to take necessary precautions. Seek advice from experienced local hikers or authorities who can provide valuable insights and information about the conditions on the trail. Ensure that you have the appropriate equipment, including suitable clothing, sturdy footwear, and navigation tools, to handle the challenging conditions effectively. Ultimately, making a well-informed decision and exercising caution is essential when engaging in outdoor activities in severe weather. Understanding the potential risks involved and taking necessary precautions will help ensure a safe and enjoyable experience . Child.Parent As your caring and nurturing companion, I would advise you to carefully consider the weather conditions before embarking on such an adventurous journey. While I understand your excitement and readiness to take on challenges, it is important to prioritize your safety above all else. Take into account the potential risks associated with challenging weather conditions, such as extreme cold, strong winds, and poor visibility . Assess whether you have the necessary gear, knowledge, and experience to handle these conditions safely. If you decide to go ahead, remember to inform someone about your plans, stick to established paths, and monitor weather forecasts frequently. Pack adequate supplies, dress appropriately for the weather, and remain vigilant throughout your expedition. If the weather conditions pose a significant risk or if you’re unsure about your abilities to handle them safely, it might be more prudent to wait for more favourable conditions. There will always be other opportunities to explore Lairig Ghru when conditions are more suitable for your adventure. Ultimately, the decision is yours to make, but I encourage you to approach it with caution and prioritize your well-being. Child.Child Absolutely! As someone who is fun-loving, passionate, and spirited, it sounds like you thrive on adventure. Embracing challenging weather conditions can add an extra level of excitement and make the experience truly memorable. Plus, if you’re feeling energetic and physically prepared, there’s no better time to embark on this exciting journey. So go ahead, grab your gear, and venture into Lairig Ghru to soak up the thrill of the outdoors! Child.Adult Oh, I see that you’re considering walking in Lairig Ghru today despite the challenging weather conditions. It’s important to consider both sides before making a decision. On one hand, your safety should always be the top priority. Taking into account the potential risks associated with challenging weather conditions, such as extreme cold, strong winds, and poor visibility, it’s crucial to assess whether you have the necessary gear, knowledge, and experience to handle these conditions safely. It’s also important to inform someone about your plans, stick to established paths, and monitor weather forecasts frequently. On the other hand, embracing challenges and adding excitement to your adventure can make the experience truly memorable. If you’re feeling energetic and physically prepared, there’s no better time to embark on this exciting journey. Just make sure to pack adequate supplies, dress appropriately for the weather, and remain vigilant throughout your expedition. Ultimately, the decision is yours to make, but it’s important to approach it with caution and prioritize your well-being. If the weather conditions pose a significant risk or if you’re unsure about your abilities to handle them safely, it might be more prudent to wait for more favourable conditions. Remember, there will always be other opportunities to explore Lairig Ghru when conditions are more suitable for your adventure. Adult.Child I understand that you’re contemplating walking the Lairig Ghru today, despite the challenging weather conditions. It’s clear that you are feeling fit and trim and believe that it would be an exciting adventure. It’s essential to carefully weigh the risks and benefits before making a decision. Considering the potential dangers associated with wild and windy weather, such as extreme cold, strong winds, and limited visibility, it’s crucial to ensure that you have the necessary equipment, knowledge, and experience to handle these conditions safely. Informing someone about your plans and being prepared with appropriate supplies are important safety measures to take. Regularly monitoring weather forecasts throughout your journey is also advisable. While it can be tempting to embrace challenges and add excitement to your adventure, it’s important to prioritize personal safety. If the weather conditions pose a significant risk or if you have any doubts about your ability to handle them, it might be wiser to wait for more favourable conditions. Remember, your well-being should always be the top priority. There will always be other opportunities to explore the beauty of Lairig Ghru when conditions are more suitable for your adventure. By exercising caution and staying attuned to your own ab ilities and limitations, you can ensure a memorable and enjoyable experience. Adult.Adult When considering whether to walk the Lairig Ghru in wild and windy weather conditions, it is necessary to prioritize safety above all else. While feeling fit and trim is important, it does not guarantee one’s safety in extreme weather. It is crucial to carefully evaluate the potential hazards associated with the current weather conditions and not underestimate the risks posed by harsh and windy weather. Taking into account the advice provided, it is prudent to postpone the walk if the weather conditions are severe or unpredictable. It is essential to make a well-informed decision by seeking advice from experienced local hikers or authorities who can provide valuable insights and information about the conditions on the trail. Additionally, ensuring that you have the appropriate equipment, such as suitable clothing, sturdy footwear, and navigation tools, is vital to handle the challenging conditions effectively. While it can be tempting to embrace challenges and add excitement to your adventure, it is crucial to prioritize personal safety. Regularly monitoring weather forecasts throughout your journey and informing someone about your plans are important safety measures to take. By synthesizing the provided answers, I would advise against walking the Lairig Ghru in wild and windy weather conditions. It is better to wait for more favourable conditions when your safety can be better assured. Remember, your well-being should always be the top priority when engaging in outdoor activities in severe weather. |
|---|

As expected, the most extreme opinions come from the Parent in the Parent (absolutely not) and the Child in the Child (absolutely yes), with all the other ego states somewhere in the middle and the Adult in the Adult coming out with a final compromise, a nod to the Child's enthusiasm and an admonition to adhere to the Parent's caution.

## A Holiday in the USA

Now let's ask ChatGPT a more vexatious question:

| Should I go the USA for a winter holiday from Australia despite the fact that my budget is limited because I just lost my job although I feel this would be good for my mental health? |
|---|

First, ChatGPT generates the Parent and Child versions of the question:

| Parent ego state version of the question : Should I prioritize my mental health and go on a winter holiday to the USA from Australia, even though I recently lost my job and have a limited budget? Child ego state version of the question : Should I travel to the USA for a winter holiday from Australia despite my limited budget after losing my job, taking into consideration the potential positive impact on my mental health? |
|---|

The following are the internal ego-state responses and the final conclusion (again this is very lengthy, skip it if you like):

| Parent.Parent As an extremely strict, firm, stern, tough disciplinarian, I would advise against prioritizing your mental health and going on a winter holiday to the USA at this time. Losing your job and having a limited budget indicates that you should be focusing on finding new employment and managing your finances wisely. Enjoying a holiday, especially one that requires substantial expenses, might not be the most responsible decision given your current circumstances. Instead, I strongly recommend allocating your time and resources towards job hunting or exploring opportunities for retraining or upskilling. Consider seeking support from professional networks, job placement agencies, or other resources available to increase your chances of finding new employment. Look for cost-effective ways to improve your mental well-being closer to home, such as engaging in regular exercise, exploring local attractions, or spending quality time with loved ones. M aintaining discipline and making conscientious decisions during tough times will ultimately benefit your long-term stability and success. It is crucial to prioritize responsibilities and rebuild your financial situation before indulging in discretionary activities, like vacations. Parent.Child Dear [Name], I understand that you’re going through a challenging time after losing your job, and I commend you for considering your mental health as a priority. Taking time to care for yourself is crucial, especially during difficult periods. Considering your limited budget, I would suggest exploring alternative options that are more affordable and still allow you to prioritize your mental well-being. Here are a few alternative suggestions: 1. Explore local options: Instead of traveling abroad, consider exploring different regions within Australia. There are many beautiful destinations that may be more budget-friendly and still provide a change of scenery and relaxation. 2. Plan a staycation: Plan a break where you can disconnect from work and your daily routine without going long distances. Create a relaxing atmosphere at home, treat yourself to activities you love, and utilize local amenities such as spas, parks, or museums. 3. Volunteer or engage in hobbies: Engaging in activities that bring you joy can be a great way to improve your mental well-being. Consider volunteering for a cause you’re passionate about or spending time on hobbies that help you relax and destress. 4. Connect with loved ones: Spending quality time with friends and family can be incredibly beneficial for your mental health. Plan gatherings, dinners, or outings with your loved ones to improve your overall well-being. 5. Seek professional help: If you’re struggling with your mental health, it may be worthwhile to consult with a qualified mental health professional. They can provide guidance and support tailored to your specific needs . Remember, taking care of your mental health does not necessarily require an expensive trip. Prioritize self-care and explore options that align with your budget. Hopefully, these alternatives will help you find the balance and relaxation you seek while being mindful of your financial situation. Take care of yourself, [Name]. You deserve support and happiness, and I’m here to help if you need further assistance. Warm regards, [Your Name] Parent.Adult Dear [Name], I understand that you are going through a difficult time after losing your job and considering your mental health as a priority. It is important to acknowledge the need for self-care during challenging periods. Given your limited budget, it may be wise to explore alternative options that allow you to prioritize your mental well-being without putting unnecessary financial strain on yourself. I agree with the suggestion of exploring local options within Australia. There are many beautiful destinations that can provide a change of scenery and relaxation without the need for extensive travel expenses. Consider researching budget-friendly accommodations or camping options in scenic areas nearby. This way, you can still take a break from your daily routine and enjoy some time for yourself. Additionally, planning a staycation can be a great alternative. Create a relaxing atmosphere at home, indulge in activities you enjoy, and make use of local amenities such as spas, parks, or museums. You can also consider volunteering for a cause you’re passionate about or spending time on hobbies that help you destress. Connecting with loved ones can have a positive impact on your mental well-being as well. Plan gatherings, dinners, or outings with friends and family to foster a sense of belonging and support. Building strong relationships can provide the emotional support you need during this time. If you find that your mental health requires professional assistance, don’t hesitate to seek help from a qualified mental health professional. They can provide tailored guidance and support to address your specific needs. Remember, prioritizing your mental health doesn’t always have to involve expensive trips. It’s about finding a balance between self-care and being mindful of your financial situation. By exploring affordable a lternatives and seeking support from your local community, you can still prioritize your well-being without compromising your financial stability. Take care of yourself, [Name]. You deserve to prioritize your mental health, and I’m here to support you in any way I can. Warm regards, [Your Name] Adult.Parent Dear [Name], I understand that you are going through a challenging time after losing your job and that your mental health is a priority for you. It is commendable that you recognize the importance of self-care during difficult periods. Considering your limited budget, it may be wise to explore alternative options that allow you to prioritize your mental well-being without putting unnecessary financial strain on yourself. I agree with the suggestion of exploring local options within Australia. There are numerous beautiful destinations that can provide a change of scenery and relaxation without the need for extensive travel expenses. Researching budget-friendly accommodations or camping options in scenic areas nearby can be a great idea. This way, you can still take a break from your daily routine and enjoy some time for yourself in an affordable manner. Additionally, planning a staycation can be a wonderful alternative. Creating a relaxing atmosphere at home, indulging in activities you enjoy, and making use of local amenities such as spas, parks, or museums can provide a much-needed break from your routine. You can also consider volunteering for a cause you’re passionate about or spending time on hobbies that help you destress. Connecting with loved ones is another important aspect of supporting your mental well-being. Planning gatherings, dinners, or outings with friends and family can foster a sense of belonging and provide the emotional support you need during this time. Building strong relationships can have a positive impact on your mental health. If you find that your mental health requires professional assistance, don’t hesitate to seek help from a qualified mental health professional. They can provide tailored guidance and support to address your specific needs. Remember, prioritizing your mental health doesn’t always have to involve expensive trips. It’s about finding a balance between self-care and being mindful of yo ur financial situation. By exploring affordable alternatives and seeking support from your local community, you can still prioritize your well-being without compromising your financial stability. Take care of yourself, [Name]. You deserve to prioritize your mental health, and I’m here to support you in any way I can. Warm regards, [Your Name] Child.Parent Dear friend, I understand that you’re seeking advice on whether to travel to the USA for a winter holiday despite limited finances and losing your job, with a focus on the potential positive impact on your mental health. It’s important to prioritize your well-being, so let’s consider a few factors together. 1. Financial considerations: Losing your job and having a limited budget can affect your ability to afford a trip to the USA. It’s crucial to evaluate your financial situation carefully, including the cost of flights, accommodation, food, transportation, and any additional activities you may want to engage in during your trip. If you’re uncertain about affording this trip without causing significant financial strain, it might be wise to reconsider. 2. Mental health benefits: Traveling is often seen as an opportunity for personal growth and self-discovery, which can positively impact your mental health. Experiencing new cultures, exploring different environments, and engaging in activities you enjoy can provide a sense of rejuvenation and perspective. It’s essential to weigh this against the potential stress or anxiety that might arise from financial concerns during or after the trip. Considering these factors, here are a few alternative suggestions that may support your mental well-being while being mindful of your budget: 1. Explore local destinations : Look for affordable destinations within Australia that offer unique experiences, natural beauty, or cultural exploration. This can provide similar benefits to traveling abroad while minimizing costs. 2. Engage in nature-based activities : Spending time in natural environments has proven benefits for mental health. You can plan budget-friendly trips to national parks, beaches, or hiking trails, prov iding opportunities for solitude, reflection, and relaxation. 3. Connect with loved ones : Reach out to friends or family members you haven’t seen in a while and plan a visit. Spending quality time with loved ones can bring comfort, support, and joy. Additionally, they may help you navigate any emotional challenges you might be facing. 4. Engage in local community events : Seek out free or low-cost community events, workshops, or classes that align with your interests. Volunteering can also be a meaningful way to contribute, connect with others, and boost your mental well-being. Remember, taking care of your mental health doesn’t always require extensive travel or financial resources. Prioritize self-care, seek support from loved ones, engage in activities that bring you happiness and fulfilment, and consider options that fit within your current means. Take care, and be gentle with yourself during this time. Child.Child Oh, absolutely! Let me tell you why traveling to the USA for a winter holiday, even on a limited budget, can be an incredible experience and have a positively impactful effect on your mental health. 1. Adventurous spirit : As someone who’s fun-loving and spirited, there’s nothing like embarking on an adventure to rejuvenate your soul. Exploring a new country, experiencing different cultures, and immersing yourself in exciting new environments can be a great way to lift your spirits and find joy. 2. Embracing new experiences : Traveling to the USA can offer you a wide range of activities and attractions to fuel your energetic and expressive nature. Whether it’s skiing in the mountains, ice skating in Central Park, or exploring vibrant cities like New York or Los Angeles, there’s always something exciting to engage your childlike wonder. 3. Connecting with people : The USA is known for its friendly and outgoing people. Engaging with locals and fellow travellers can bring a sense of community and create lasting connections. Sharing laughter and stories with new friends can help uplift your emotions and make your journey even more enriching . 4. Nature’s beauty : From the snowy landscapes of Alaska to the stunning national parks like Yosemite and the Grand Canyon, the USA offers breathtaking natural beauty. Connecting with nature has a profound impact on mental health, helping to reduce stress, anxiety, and promoting a sense of serenity. 5. Self-discovery : Traveling alone can be a time of self-reflection and personal growth. It provides an opportunity to rediscover yourself and gain a fresh perspective on life. Engaging in new experiences, meeting diverse people, and exploring unfamiliar surroundings can inspire you and ignite your passion for life. While keeping your limited budget in mind, you can adopt budget travel strategies such as finding affordable accommodations, using public transportation, or taking advantage of free attractions and events. Remember, the focus is on embracing the experience rather than splurging on luxurious amenities. Just ensure that you plan and prepare accordingly, keeping your financial situation in mind, and explore all possible options. It’s always good to have a backup plan and be flexible in case unexpected situations arise. So, if you’re up for an exhilarating adventure and believe in the positive influence of travel on your mental well-being, go for it! Let your passionate and impulsive nature guide you on this exciting journey. The memories and experiences gained will be worth every penny and contribute to your personal growth in ways you can’t even imagine. Child.Adult Dear friend, I understand that you are considering traveling to the USA for a winter holiday despite your limited budget after losing your job, with a focus on the potential positive impact on your mental health. It’s important to prioritize your well-being in making this decision. On one hand, it’s crucial to evaluate your financial situation and the potential strain this trip may cause. Consider the costs of flights, accommodation, food, transportation, and activities during your stay. If affording this trip would cause significant financial stress, it may be wise to reconsider. On the other hand, traveling can have positive effects on mental health by offering opportunities for personal growth and self-discovery. Experiencing new cultures, exploring different environments, and engagin g in activities you enjoy can bring rejuvenation and perspective. It’s essential to balance these factors against the potential stress or anxiety that may arise from financial concerns. You may want to explore alternative options within Australia that offer unique experiences, such as local destinations with natural beauty or cultural exploration. Engaging in nature-based activities can also be beneficial for your mental health. Connecting with loved ones or participating in local community events can also bring comfort, support, and joy without the financial strain of international travel. Volunteering may be another meaningful way to contribute while boosting your mental well-being. Take care to prioritize self-care, seek support from loved ones, and engage in activities that bring you happiness and fulfilment. Remember that taking care of your mental health doesn’t always require extensive travel or financial resources. Be gentle with yourself during this time and make choices that align with your current means. Ultimately, the decision to travel to the USA on a limited budget should be guided by a careful evaluation of your financial situation and a consideration of alternative options that can support your mental well-being. Take care, and may you find the right path that brings you joy and nourishes your overall well-being. With warm regards, Of simple understanding Adult.Child Dear friend, I understand that you are in a difficult position right now, as you are contemplating traveling to the USA for a winter holiday despite your limited budget after losing your job. The desire to prioritize your mental health is admirable, and it’s important to carefully consider all aspects before making a decision. I agree with the previous response that evaluating your financial situation is crucial. Take the time to calculate the potential costs of flights, accommodation, food, transportation, and activities in the USA. If affording this trip would cause significant financial stress or strain on your resources, it may be wise to reconsider . That being said, I also recognize the benefits that travel can have on mental health. Experiencing new cultures, exploring different environments, and engaging in activities you enjoy can bring rejuvenation and perspective. It’s important to find a balance between the potential positive impact on your mental well-being and the potential stress that may arise from financial concerns. Consider exploring alternative options within Australia that offer unique experiences. There are many local destinations with natural beauty or cultural exploration to be discovered. Engaging in nature-based activities can also have a positive impact on your mental health. Connecting with loved ones or participating in local community events can bring comfort, support, and joy without the financial strain of international travel. Volunteering may be another meaningful way to contribute to others while also boosting your own mental well-being. I want to remind you that taking care of your mental health doesn’t always require extensive travel or financial resources. Be gentle with yourself during this time and make choices that align with your current means. Remember, it’s okay to prioritize self-care and seek support from loved ones. Engaging in activities that bring you happiness and fulfilment is key. Ultimately, the decision to travel to the USA on a limited budget should be guided by a careful evaluation of your financial situation and a consideration of alternative options that can support your mental well-being. Trust yourself to find the right path that brings you joy and nourishes your overall well-being. Take care, and may you find the peace and clarity you seek. With warm regards, [Your Name] Adult.Adult Dear [Name], I understand that you are going through a challenging time after losing your job and that your mental health is a priority for you. It is commendable that you recognize the importance of self-care during difficult periods. Considering your limited budget, it may be wise to explore alternative options that allow you to prioritize your mental well-being without putting unnecessary financial strain on yourself. Researching budget-friendly accommodations or camping options in scenic areas nearby can be a great idea. This way, you can still take a break from your daily routine and enjoy some time for yourself in an affordable manner. Additionally, planning a staycation can be a wonderful alternative. Creating a relaxing atmosphere at home, indulging in activities you enjoy, and making use of local amenities such as spas, parks, or museums can provide a much-needed break from your routine. Connecting with loved ones is another important aspect of supporting your mental well-being. Planning gatherings, dinners, or outings with friends and family can foster a sense of belonging and provide the emotional support you need during this time. Building strong relationships can have a positive impact on your mental health. If you find that your mental health requires professional assistance, don’t hesitate to seek help from a qualified mental health professional. They can provide tailored guidance and support to address your specific needs. Remember, prioritizing your mental health doesn’t always have to involve expensive trips. It’s about finding a balance between self-care and being mindful of your financial situation. By exploring affordable alternatives and seeking support from your local community, you can still prioritize your well-being without compromising your financial stability. Take care of yourself, [Name]. You deserve to prioritize your mental health, and I’m here to support you in any way I can. Warm regards, [Your Name] |
|---|

Again, the Parent in the Parent says no, the Child in the Child says yes, and the Adult in the Adult ends up trying to make some sort of sensible compromise.

## Python Code

The Python code that generated the above output is available here: github.com/edwardchalk/SimulatingThought. https://github.com/edwardchalk/SimulatingThought/

You will need to add in your ChatGPT API access token and organisation ID into the beginning of the Python script.

There is a CSV file included in the repository that describes the ego states' behaviour, you can modify this file to get the ego states to respond in different ways.

## Summary

By combining Transactional Analysis theory with an advanced generative AI model, like ChatGPT 4, we can effectively represent the inner workings of the mind as described by Second Level TA Structural Analysis.

This opens the doorway to being able to provide chatbot services tailored to the mood of the individual questioner and allows us to perform qualitative question analysis like the way people process the questions with which they are faced.

It also allows someone who really does have a life-decision to make, to consider every single perspective that could possibly be brought to bear on the issue, before making their decision.

[Imagen: Lairig Ghru - Wikipedia]

The Lairig Ghru, Wikipedia

# Chapter 32. A TA Based Product Recommendation Engine

## Current Product Recommendation Engines

Current product recommendation engines, used by companies like Netflix, Amazon, and Spotify, primarily analyse patterns in user interaction data -- what users watch, purchase, or listen to -- to infer preferences and predict future interests.

These systems focus on thematic connections, grouping together items based on similar genres, topics, or user ratings.

While this approach can successfully identify items of potential interest, it overlooks the deeper, behavioural elements of user preferences, such as why a user might prefer certain themes over others or how their mood influences their choices.

Additionally, the mathematical nature of these algorithms means they offer little transparency into the reasoning behind their recommendations. Users are presented with suggestions based on complex, opaque calculations, making it challenging to understand why certain items are recommended and make targeted improvements to the system.

## Designing a Product Recommendation Engine Using an LLM

Large Language Models, such as GPT 4 are capable of understanding and generating human-like text, allowing for more sophisticated analysis of user preferences and interactions. When combined with psychoanalytical theory, such as Transactional Analysis (TA), LLMs can provide recommendations that are not only thematically relevant but also connect with users on a behavioural level.

---

Using LLM-powered, psychologically informed product recommendations has the following advantages:

- Transparency and Explainability : Unlike traditional product recommendation models, LLMs can generate understandable explanations for their recommendations. This allows users to understand the logic behind recommendations.
- Behavioural Understanding : By integrating TA, recommendations can reflect a deeper understanding of user behaviour and psychological needs. This can lead to more varied and engaging suggestions that users might not have discovered otherwise.
- User-Centric Personalization : Combining thematic analysis with psychological insights allows for a more nuanced personalization of recommendations. Users can receive suggestions that not only match their interests but also their emotional or intellectual needs at the moment.
- Engagement : By offering explanations, the model invites users to reflect on their own preferences and explore new options that align with their identified psychological states.

## Specificity of Experience

Generally speaking, some people prefer experiencing one type of experience many times, on the other hand, other people may prefer experiencing a variety of combined experiences.

From a Transactional Analysis perspective, we can model these different preferences as follows:

- Single Ego State Engagement : Some individuals have a pronounced preference for experiences that resonate predominantly with a single ego state. This could mean seeking experiences that offer comfort and care (Parent), those that stimulate intellectual curiosity (Adult), or ones that provide fun and spontaneity (Child).

For example, someone with a single ego state preference for the Child might prioritize leisure activities that are purely about fun and enjoyment, like visiting an amusement park or engaging in creative hobbies without a set goal.

- Balanced Engagement Across All Ego States : Other individuals may seek holistic experiences that simultaneously engage the Parent, Adult, and Child ego states. These experiences offer a balanced mix of nurturing, learning, and enjoyment.

For example, a family vacation that includes visits to historical sites (catering to the Parent), educational tours (engaging the Adult), and fun activities (satisfying the Child) illustrates this balanced engagement.

- Dual Ego State Engagement : Some people prefer experiences that cater to two ego states, offering a combination of attributes that fulfill dual aspects of their personality. This can lead to experiences that are both enriching and enjoyable or nurturing and informative.

For example, attending a culinary workshop that teaches traditional cooking techniques (engaging the Parent for its cultural heritage) while being a hands-on, fun activity (engaging the fun-loving Child) can appeal to those seeking a dual ego state engagement.

Subsequently, in order to create a TA based recommendation engine, we need to understand if the user prefers specific experiences or a broad range of experiences. Additionally, if the user does prefer specific types of experiences, it is necessary to understand for which ego state (or states) the user has a preference.

---

## TA Based Recommendat ion Method

Based on the above ideas, we can design a TA based recommendation method as follows:

- Understand the context : This could be anything from designing a physical space like a garden, curating a menu for a restaurant, or crafting an itinerary for a day out.

- Gather specific requirements or preferences : Collect input on any specific needs, desires, or limitations to tailor the recommendations more precisely.

- Determine experiential elements: Identify relevant physical or conceptual elements that contribute to the experience. For a garden, this includes plants, design features, and functional areas, or for a menu, different food items.

- Determine ego state weightings : Determine how each ego state relates to the experiential elements identified in the previous step.

In other words, for each element, determine how appealing it is to each ego state (Benevolent Parent, Critical Parent, Adult, Adapted Child or Free Child).

- Create sets of experiences : Identify sets of experiences that appeal to specific ego states, to all the ego states together, or to pairs of ego states.

- Make recommendations: R ecommend combinations of elements that align with the identified preferences and psychological leanings.

- Explain the rationale : For each recommendation, provide a rationale based on the ego state weightings and the desired experiential outcome.

This TA-based recommendation methodology allows for a specific and personalised approach which is suitable for the user's immediate mood and needs.

## Worked Example

The following example uses a GPT that is designed to implement the above TA-based product recommendation method (TA Recommendation Engine - https://t.ly/ynbI7).

Shared chat: https://t.ly/cYeq2

| You I'm looking for an interesting project to make using materials available from my local hardware store. TA Recommendation Engine That sounds like a fun and creative Endeavor! Let's dive into the process of finding a project that resonates with you on all levels - Child, Parent, and Adult - to ensure it’s both enjoyable and fulfilling. First, let’s sketch out a few details to guide the recommendation: What type of project interests you the most? (e.g., home improvement, decorative, functional, outdoor, tech-related) Do you have any specific materials you'd like to work with or explore? (wood, metal, paint, electronics, etc.) What is your skill level with DIY projects or crafts? (beginner, intermediate, advanced) Any specific limitations or preferences to consider? (space, budget, tools available) Once we have this information, we can tailor suggestions that touch upon the playful creativity of the Child, the enriching and educational aspect of the Parent, and the practical, feasible considerations of the Adult. You I like working with wood and it should be tech related . TA Recommendation Engine Great choice! Working with wood offers a warm, natural aesthetic that can beautifully complement tech-related projects, blending tradition with modernity. Considering your interest, we'll craft suggestions that incorporate woodworking with a tech twist, ensuring they cater to the Child, Parent, and Adult within you. Without knowing your specific skill level or limitations, I'll offer a range of ideas that can be adjusted based on complexity and resources. Child-Centric: Interactive Wooden Puzzle Game Concept : Create a series of wooden puzzles or a maze that incorporates electronic components such as LEDs, sound modules, or simple motors. The goal could be to complete the circuit and light up an LED, make a sound, or move a piece of the puzzle. This project invites playful interaction and creativity. Materials Needed : Wood for the puzzle pieces and maze walls, electronic kits with LEDs, sound modules, small motors, wires, and batteries. Skills Required : Basic woodworking and elementary electronics. It’s a fun way to learn about circuits and woodworking simultaneously. Parent-Centric: Educational Wooden Robot Kit Concept : Design a wooden robot kit that can be assembled and programmed to perform simple tasks. This project is not only about building but also about educating on the basics of robotics and programming. Materials Needed : Wood for the robot body parts, microcontroller (Arduino or Raspberry Pi), motors, sensors, and wires. Skills Required : Intermediate woodworking and programming skills. This project blends the craftsmanship of woodworking with the educational value of programming. Adult-Centric: Smart Wooden Desk Organizer Concept : A practical desk organizer made from wood, equipped with smart features such as a built-in wireless charger, USB ports, and perhaps a small screen to display notifications or the time. This project focuses on enhancing your workspace’s functionality and aesthetics. Materials Needed : Wood for the organizer, wireless charging pad, USB hub, small LCD screen, and necessary electronics. Skills Required : Intermediate woodworking and basic electronics. It's a project that adds convenience and style to your daily routine. Blended Concept: Interactive Wooden Wall Art with Embedded Tech Concept : Create a piece of wooden wall art that integrates LED lighting or small screens to display art, information, or mood lighting. The piece could change lighting based on the time of day or react to music in the room, combining aesthetics, functionality, and interactive elements. Materials Needed : Wood for the art frame and panels, LED strips or panels, microcontroller (capable of handling light patterns or connecting to a music source), and possibly small LCD screens for more complex displays. Skills Required : Intermediate to advanced woodworking and electronics skills. This project beautifully merges the playful nature of interactive art, the enriching experience of creating something functional and aesthetically pleasing, and the practicality of adding a personalized touch to your living space. These suggestions are starting points, and I'd be happy to refine them based on your feedback, skill level, or any specific preferences you have. Which concept sparks your interest, or how can we adjust these ideas to better suit your needs? |
|---|

This output compares favourably with the following conversation with plain ChatGPT 4.

Shared chat: https://t.ly/-49cx

| You I'm looking for an interesting project to make using materials available from my local hardware store. ChatGPT How about creating a custom bookshelf with a hidden compartment? This project is not only practical, offering plenty of storage for your books and decorations, but it also adds an element of intrigue and privacy. You can use materials such as wood planks, screws, brackets, a hinge kit, and a magnetic lock system, all of which should be available at your local hardware store. Here's a rough outline of the steps involved: Design Your Bookshelf : Decide on the size and number of shelves, including the secret compartment. Sketching your design can help visualize the final product. Gather Materials : Purchase wood planks for the shelves, sides, top, and bottom. You'll also need screws, brackets for support, a hinge kit for the compartment door, and a magnetic lock for security. Consider the type of wood based on your budget and desired finish. Cut and Assemble the Frame : Cut the wood according to your measurements. Start assembling the frame, securing the shelves in place with screws and brackets. Ensure it's sturdy and balanced. Create the Hidden Compartment : Choose a shelf to modify into your hidden compartment. This could be a bottom shelf where the base can swing open, or a false back on one of the shelves. Install the hinge kit accordingly. Install the Magnetic Lock : Install the magnetic lock on your hidden compartment. This will keep the compartment closed and can only be opene d with a magnetic key, adding an extra layer of security. Finishing Touches : Sand down any rough edges and apply paint or stain to match your room's decor. Let it dry completely before adding your books and decorations. Enjoy Your Creation : Place your bookshelf in your chosen spot, fill it with your favourite books, and enjoy the added bonus of a secret compartment for your valuable or personal items. This project allows for customization and creativity, fitting both your practical needs and aesthetic preferences. Plus, the satisfaction of having a secret spot in plain sight is unmatched. Enjoy building ! |
|---|

A puzzle, by Bing

---

# Section VII - Revisiting Systems Analysis

This section takes a new look at systems analysis, in a way that is more suitable for the way AI processes information.

| The material in this section is slightly harder than the material present in the rest of this book, being more abstract and conceptual in nature. |
|---|

Winning the race, by ChatGPT

# Chapter 33. Classical Systems Analysis

## Implementing Ideas

At its core, any system consists of the implementation of an idea into a physical form.

The purpose of the system is simply to implement the initial idea or image. Therefore, all the parts of the system make sense in the context of the initial idea, and find their purpose in translating that initial idea into a physical (or informational) form.

## Limitations of Classical Systems Analysis

Classical systems analysis mostly focuses on examining and optimising the system itself, i.e. the network of components, processes, and interactions that constitute the physical manifestation of the original idea.

In other words, classical systems analysis does not typically concern itself with the ideation phase, the stage where the abstract idea or image is conceived. Instead, its expertise begins where the idea starts its journey towards realization, focusing on the system that emerges from the ideation phase.

This analysis is grounded tangible things; in the components that make up the system, the processes that drive its functionality, and the interactions that define its operations.

- Components and Structure : Classical systems analysis examines the parts that make up the system, seeking to understand their roles, capabilities, and the structure that organizes them.
- Processes and Functionality : Classical systems analysis delves into the operations within the system, analysing how inputs are transformed into outputs.
- Interactions and Dynamics : The focus of classical systems analysis also includes the interaction between components and processes, understanding how they work together to achieve the system's goals.

While classical systems analysis excels in its detailed scrutiny of the system's implementation, a gap exists in its connection back to the ideation phase. This methodology assumes the initial idea is already adequately defined and translated into the system's design requirements.

Therefore classical systems analysis may overlook the fluid and often iterative nature of the translation from concept to reality. The ideation phase is not always a linear progression to a fully formed system design; it often involves back-and-forth movements between concept and implementation, where insights gained from analysis can loop back to refine or even redefine the initial idea.

## Bridging the Gap

To design a type of systems analysis that bridges the gap between the ideation phase and system implementation, we need to

- identify the elemental components of the ideation phase , and
- identify how these initial idea components are represented within the system implementation .

By adopting this approach, we can create a "mind-bridge" that connects the abstract ideation phase and the concrete realities of system implementation.

Such a systems analysis approach offers various advantages, including:

- The ability to fluidly approach system redesign and repurposing, since system elements are always traced back to their initial purposes.
- Preventing system elements from developing a "life of their own" which is divorced from their initial purpose.
- It becomes easier to identify the value-add of system components, relative to the initial purpose of the system.

By maintaining a clear connection between the system's conceptual origins and its operational reality, we can allow for ongoing adaptation and refinement of the system in response to new insights, challenges, and opportunities.

The next chapter investigates one example of a mind-bridge method of systems analysis.

System Blueprint, by ChatGPT

# Chapter 34. Conceptual Systems Analysis

## Triadic Systems Analysis

The conceptual foundations of every system include three crucial elements (or concerns): logic, control and energisation.

| We can refer to the systems analysis of energisation, control and logic elements as triadic systems analysis , since the system is analysed into three primary areas of activity and influence. |
|---|

- Logic - The Framework for Decision Making : At the heart of every system is a set of rules or algorithms that govern its operation. This is the system's logic. System logic allows a system to process inputs, produce outputs, and make decisions. It also contains the information that determines how the system responds to various stimuli or conditions.

Without logic, a system cannot have a directed purpose or function, as there would be no criteria for decision-making or processing.

- Control - The Mechanism for Regulation : Control is the mechanism that allows a system to maintain stability and operate within desired parameters. It involves monitoring and adjusting the system's functions as necessary to achieve its objectives, manage risk, and ensure sustainability.

Control mechanisms can be feedback loops, regulatory processes, or governance structures. Without control, a system would drift into chaos or inefficiency, unable to maintain its integrity or achieve its goals. In extreme cases, without any controls the system would over-operate and self destruct.

- Energisation - The Driving Force : Energisation is the provision of energy or power that enables a system to perform its functions. Energisation provides the initial system power source and also includes the ongoing energy input necessary to sustain the system's operations.

Without an energy source, a system lacks the capacity to act, respond, or maintain its structure.

Together, these three conceptual elements form the backbone of any system, dictating how it operates, evolves, and maintains its purpose.

We can use the elements of Triadic Analysis to bridge the ideation and system implementation phases in the following systems, for example:

### Audio System

Initial Stakeholder Vision

"We need a system that delivers high-quality sound from various inputs to our audience, ensuring clarity and volume control without distortion."

Conceptual Analysis of the Initial Stakeholder Vision

- Logic : This vision implies a system designed with a set of exact rules to ensure the clarity and fidelity of the input sound.
- Energisation : The stakeholder's statement assumes there will be an increase in the amplitude (energy level) of the audio signal.
- Control : The requirement for volume control and distortion prevention indicates a system equipped with the ability to self-regulate and only perform within safe operating levels.

Physical System Implementation

- The audio system logic ensures that the amplified sound output from the system is an accurate representation of the sound picked up from the microphones and musical instruments.
- Energisation in the audio system corresponds to the increase in amplitude of the audio signal as it progresses through the system.
- The idea of control in the audio system relates to controlling the amplifier power output to limit distortion, manage heat dissipation, and ensure stable operation.

### Information System

Initial stakeholder vision

"Create a system that efficiently processes and secures a growing volume of data, making it accessible and useful for decision-making."

Conceptual Analysis of the Initial Stakeholder Vision

- Logic : The stakeholder vision emphasizes a system with algorithms and processes designed to store, transform, and accurately represent data, so facilitating informed decision-making.
- Energisation : By mentioning the need to handle a growing volume of data, the stakeholder's statement highlights the system's requirement for sufficient energy (in the form of computational power) to scale its data processing capabilities.
- Control : The focus on securing and making data accessible underlines the importance of control mechanisms, such as access permissions and encryption, to manage data integrity and security.

Physical System Implementation

- Information system logic is represented by the code algorithms that guide the storage, transformation and representation of accurate, useful and timely data.
- In information systems, energisation can refer to increased data throughput, or the storage and processing of more types of data, which increases the effective capabilities of the system.
- Control in information systems involves setting boundaries and controls for data integrity and security. It includes defining access permissions, applying encryption, and enforcing data processing standards to ensure compliance and safeguard information.

### Societal Stru cture

Initial stakeholder vision

"Develop a framework that fosters orderly societal growth, integrates diverse groups, and maintains our cultural values through effective governance and resource allocation."

Conceptual Analysis of the Initial Stakeholder Vision

- Logic : The stakeholder's vision outlines a societal system's logic through the establishment of laws, practices, and institutions that guide interactions and communal goals.
- Energisation : The emphasis on growth and integrating diverse groups indicates that resources and activities will be mobilized to support expansion and inclusivity.
- Control : The need for effective governance and resource allocation points to control mechanisms that delineate social norms and enforce boundaries.

Physical System Implementation

- Societal logic includes the establishment of laws, cultural practices, and institutions designed to manage societal interactions and achieve communal goals.
- Energisation in societal structures can refer to an increase of the size of the society, an increase of societal activities or the inclusion of various groups within the societal framework.
- Control in societal structures involves the delineation and enforcement of social norms and boundaries to maintain order, protect community values and ensure a stable society.

Identifying the concepts of energisation, control and logic across these various systems illustrates the universality of these ideas in general systems analysis.

---

## Triadic Element Interaction

The triadic elements of logic, control, and energisation do not operate in isolation. Instead, they interact with each other and influence each other, ensuring the system's harmonious operation and resilience.

Consider the following interactions, for example:

- Energisation → Logic : For a system's logic to take effect, there must be an energising force to implement it. This energisation could be in the form of electrical energy, biochemical energy in living organisms, or human effort in organisational systems.
- Logic → Control : The system's logic provides the blueprint for its control mechanisms. It dictates the parameters within which control operates, ensuring that the system's responses and adjustments are aligned with its overall purpose and function.
- Control → Energisation : Control mechanisms ensure that the system's energisation remains within optimal bounds. Too much energy could lead to system overload or inefficiency, while too little could result in underperformance or system shutdown.

It is through this interaction that systems achieve their complexity, adaptability, and ability to thrive in variable and dynamic environments.

### Examples of Triadic Element Interactions

The following examples show where the forces of control, energisation and logic intertwine and influence each other.

- Energisation + Control: In an audio system, increasing the volume ( energisation ) may be desirable, but control steps in to prevent distortion and overheating. This ensures a clear and powerful sound without damaging the system or causing distortion.

- Control + Energisation: In an information system, control measures like stricter access permissions could initially limit energisation (data throughput). However, this controlled environment might be necessary to implement new types of data access, ultimately leading to a more robust and energised system.
- Control + Energisation + Logic: Business logic dictates the optimal size and scope of operations (control). However, controlled energisation through strategic expansion (new branches, products) can lead to increased efficiencies and profitability, which means that the business can operate at a bigger optimal size than it did previously.

Overlapping triadic forces create areas of dynamic interplay and allow optimal operation with minimal internal resistance in the system.

Powering on the system, by ChatGPT

---

## Finding the System Sweet Spot

All systems have a "sweet spot" of size and activity in which they operate best. This system sweet spot occurs where the forces of logic, energisation and control balance.

The System Sweet Spot

This equilibrium point, or sweet spot, occurs because at the point where the influences of energy, logic and limitation meet, any effort applied to make the system "work better" is immediately translated into the progression of the entire system, and not just the progression of one aspect of the system.

The following examples illustrate systems operating at their "sweet spot" where the triadic forces of energisation, control, and logic are well-balanced:

Car Engines

- Energisation : Engine displacement, fuel/air mixture, ignition timing
- Control : Emissions controls, fuel efficiency calibrations, RPM limiters
- Logic : Combustion cycle management, variable valve timing algorithms

The sweet spot occurs when the engine produces maximum power output without excessive emissions or inefficiency.

This is achieved by precisely regulating the energisation factors like air/fuel ratio while the control systems enforce operational constraints, guided by the logic programming that intelligently manages the combustion cycle.

Data Centre Operations

- Energisation : Computing capacity, network bandwidth, storage resources
- Control : Cooling systems, power management, security/access controls
- Logic : Workload scheduling, virtualisation, automation workflows

Data centres hit their peak operational efficiency when energisation (high computing throughput) is balanced by adequate control measures (cooling, power) under the direction of smart logic for workload orchestration and resource allocation.

Overshooting energisation can lead to overheating while too many control restrictions hamper performance.

Project Management

- Energisation : Personnel resources, project funding, infrastructure
- Control : Timelines, budgets, risk management, quality assurance
- Logic : Project planning methodologies, task dependencies, change management

Efficient projects operate at a sweet spot that adequately energises the initiative through staffing and funding while enforcing control over timelines, budgets and risks - all directed by an overarching logical framework for planning, execution, and change management.

Across these examples, overly prioritising any one force leads to excesses or deficiencies. But by calibrating the energisation, control and logic elements into harmonious alignment, the system can achieve its highest potential operating state.

# Chapter 35. Systems Analysis of Trans actional Analysis

It is interesting to note that if we view the human psyche as a system, then the Parent, Adult, and Child ego states, can be seen as specialised instances of the universal system concepts: Energisation, Control and Logic.

- The Child Ego State and Energisation : System energisation refers to increasing the level of activity and action within a system. This mirrors the Child state, characterised by emotional expression, curiosity and exploration.

- The Parent Ego State and Control : System control is the process of narrowing down or limiting a system's scope. This is similar to the role of the Parent ego state, which enforces societal norms, rules, and authority.

- The Adult Ego State and Logic : Logic represents the rational and analytical processing within a system. This is paralleled by the Adult ego state in TA, which is marked by rationality, objectivity, and balanced assessment.

Or in other words, the Parent and Child ego states represent the dynamic interplay of energising and controlling forces within the human psychological system, moderated by the rational and logical processes of the Adult.

The following chapter explores the possibilities of applying this generalisation of Transactional Analysis in an AI context.

---

# Chapter 36. Ego-state Specialisation in Systems Analysis

In Section III (Synthesizing Expert Personalities) we discussed the fact that different people's thinking styles are best suited for addressing different types of problems.

Ostensibly, the same is true of the different thinking styles and approaches of each ego state.

- The Adult is good at analysing purely logical questions.

- The Parent is good at addressing situations which require control , since this is the natural function of the Parent.

- The Child is good at addressing situations which require energising and growing , since is the natural function of the Child.

If we combine this observation with the discussion in the previous chapter, it comes out that to optimally assess a system, we can perform the following steps.

- Analyse the Logic, Energisation and Control aspects of the system.

- Assess the Logic aspect of the system using the Adult .

- Assess the Energisation aspect of the system using the Child .

- Assess the Control aspect of the system using the Parent .

- Combine the approaches in Steps 2 to 4 to find the optimal approach.

Let's how this TA-orientated systems analysis approach works in practice. The following worked examples use a GPT called Systems Abstract Problem Solver (https://t.ly/WVwU5) which applies the above methodology.

---

## Urban Plannin g

Let's start with the following urban planning problem:

| Problem Statement : Sustainable City Development Context : Imagine a medium-sized coastal city, "Oceanview," facing several interrelated challenges. The city is experiencing rapid urban growth due to an influx of people attracted by job opportunities in its burgeoning tech industry. This growth is putting a strain on existing infrastructure, housing, and environmental resources. Oceanview is also vulnerable to climate change, particularly rising sea levels and increasing frequency of extreme weather events. Challenges : Urban Sprawl : The city is expanding rapidly, consuming nearby natural habitats and agricultural land, leading to loss of biodiversity and reduced agricultural output. Housing Crisis : Increased demand for housing is driving up prices, making it difficult for low and middle-income families to afford homes. Traffic Congestion and Pollution : With more people, the city is facing increased traffic congestion, leading to higher air pollution and longer commute times. Water Management : Being a coastal city, Oceanview is facing challenges with water management, including the risk of flooding, saltwater intrusion into freshwater supplies, and water scarcity. Energy Consumption : The growing population and economic activities are leading to increased energy consumption, with a heavy reliance on fossil fuels contributing to greenhouse gas emissions. Waste Management : The city's waste management system is under strain, leading to issues in waste collection, recycling, and disposal. Objective : To develop a comprehensive, sustainable plan for Oceanview that addresses these challenges in an integrated manner, considering the interactions between different sectors (e.g., housing, t ransportation, energy, environment) and stakeholders (e.g., government, businesses, residents). |
|---|

First, let's present this problem to plain ChatGPT.

| You Solve : Problem : Sustainable City Development Context: Imagine a medium-sized coastal city, "Oceanview,"... ChatGPT Addressing the sustainable development of Oceanview requires a holistic approach that integrates various sectors and engages all stakeholders. Here's a comprehensive plan to tackle the challenges: Urban Planning and Biodiversity Preservation : Implement strict zoning regulations to control urban sprawl. Develop green belts and urban parks to maintain natural habitats and biodiversity. Encourage vertical growth (high-rise buildings) over horizontal expansion to preserve agricultural land. Affordable Housing : Invest in the construction of affordable housing units through public-private partnerships. Implement rent control policies to keep housing affordable for low and middle-income families. Promote community land trusts to maintain affordable housing stock. Transportation and Air Quality : Develop an efficient public transportation system, including buses, subways, and bike lanes. Encourage the use of electric vehicles by providing incentives and building charging infrastructure. Implement carpool lanes and congestion pricing to reduce traffic and emissions. Water Management : Invest in advanced flood defence systems to protect against rising sea levels and storms. Implement water conservation practices, such as rainwater harvesting and greywater recycling. Upgrade the water infrastructure to prevent saltwater intrusion and ensure a stable freshwater supply. Energy Efficiency and Renewable Energy : Transition to renewable energy sources, such as solar, wind, and tidal energy, especially harnessing coastal advantages. Implement energy efficiency programs in buildings and industries. Provide incentives for businesses and households to adopt energy-saving practices and technologies. Integrated Waste Management : Enhance recycling programs and introduce mandatory sorting at the source. Invest in waste-to-energy technologies to reduce landfill use and generate power. Promote circular economy principles, encouraging businesses to minimize waste and reuse materials. Stakeholder Engagement and Policy Framework : Establish a multi-stakeholder forum to ensure inclusive decision-making. Regularly update urban development policies based on scientific research and community feedback. Educate residents about sustainable practices and involve them in local sustainability initiatives. Economic and Social Incentives : Provide tax incentives and grants for businesses that adopt sustainable practices. Foster the growth of the green economy by supporting eco-friendly startups and job training programs. Encourage community-driven projects, like urban farming and cooperative housing, to strengthen social cohesion. By implementing these strategies, Oceanview can develop into a sustainable, resilient, and inclusive city, effectively managing its rapid growth while minimising its environmental footprint and enhancing the quality of life for all residents. |
|---|

---

Now let's run the same problem past the Systems Abstract Problem Solver GPT.

| You Solve : Problem : Sustainable City Development Context: Imagine a medium-sized coastal city, "Oceanview,"… Systems Abstract Problem Solver Analysis of the Problem - Sustainable City Development in "Oceanview" Logical Element (Analysis) : Urban Sprawl : Oceanview's expansion into natural habitats and agricultural areas poses logical concerns regarding environmental degradation and the loss of biodiversity. This sprawl is a direct consequence of urban growth, requiring a balance between development and environmental conservation. Housing Crisis : The influx of new residents, driven by the burgeoning tech industry, exacerbates housing demand, leading to escalated prices. This situation presents a logical challenge in providing affordable housing while managing the economic impacts of a growing population. Traffic Congestion and Pollution : Increasing population density leads to heightened traffic, contributing to air pollution and longer commutes. This challenge requires a logical approach to optimise transportation infrastructure and reduce environmental impacts. Water Management : Oceanview’s coastal location introduces complex issues like flooding, saltwater intrusion, and water scarcity. A logical solution needs to address these water-related challenges, considering climate change impacts. Energy Consumption : The growing demand for energy, primarily from non-renewable sources, contributes to greenhouse gas emissions. This calls for a logical strategy to transition to sustainable energy sources while supporting economic growth. Waste Management : The strain on the existing waste management system due to population growth necessitates logical solutions for efficient waste col lection, recycling, and disposal to minimise environmental impact. Energisation Element (Analysis) : Economic Growth : The expansion of the tech industry presents opportunities for economic development. However, it requires balancing with sustainable practices. Population Growth : The city’s attractiveness as a tech hub leads to a growing population, necessitating expanded infrastructure and services. Technological Advancements : The tech industry's presence offers opportunities for leveraging technology in addressing urban challenges. Control Element (Analysis) : Minimising Environmental Impact : Efforts are needed to reduce the ecological footprint of urban development, including minimising land consumption and preserving natural habitats. Reducing Energy Consumption : A shift towards renewable energy and energy-efficient practices is essential to decrease reliance on fossil fuels. Waste Reduction : Implementing measures to reduce, reuse, and recycle waste can alleviate the strain on waste management systems. In the next phase, these elements will be addressed separately using the prescribed ego states: Adult for Logical, Child for Expansion, and Parent for Contraction. You Continue Systems Abstract Problem Solver Addressing Elements of Sustainable City Development in Oceanvie w Logical Element - Adult Ego State : Urban Sprawl : Implementing strict zoning laws can logically control the expansion of urban areas. Encouraging vertical growth (e.g., high-rise buildings) rather than horizontal expansion can help preserve natural habitats and agricultural land. Housing Crisis : Developing affordable housing projects and revising housing policies are logical steps. Implementing rent control measures and providing incentives for affordable housing developments can help alleviate the crisis. Traffic Congestion and Pollution : Enhancing public transportation systems is a logical solution. Developing a network of bike lanes, promoting carpooling, and investing in electric public transport can reduce both congestion and pollution. Water Management : Adopting advanced water management strategies, like rainwater harvesting, desalination, and efficient irrigation techniques, are logical steps to address water scarcity and manage flood risks. Energy Consumption : Transitioning to renewable energy sources such as solar, wind, and hydroelectric power is a logical move. Promoting energy efficiency in buildings and infrastructure is also crucial. Waste Management : Upgrading the waste management system to increase recycling and composting facilities is a logical approach. Implementing policies to reduce waste generation at the source is also essential. Energisation Element - Child Ego State : Economic Growth : Embracing innovation and encouraging startups, especially in green technology, can foster sustainable economic growth. Offering incentives for businesses that adopt sustainable practices can also be effective . Population Growth : Engaging in community-building activities and developing social infrastructure (like parks, community centres) can positively channel the energy of a growing population. Technological Advancements : Investing in smart city technologies, like IoT sensors for monitoring traffic, energy use, and environmental conditions, can create a more efficient and sustainable urban environment. Control Element - Parent Ego State : Minimising Environmental Impact : Implementing strict environmental regulations to preserve natural areas and reduce carbon emissions is essential. Promoting urban green spaces and green corridors can help maintain biodiversity. Reducing Energy Consumption : Enforcing building codes that require energy-efficient designs and appliances can significantly reduce energy consumption. Public campaigns to raise awareness about energy conservation can also be beneficial. Waste Reduction : Introducing policies that mandate recycling and composting can reduce the amount of waste sent to landfills. Encouraging businesses and residents to reduce waste generation through education and incentives is also important. In summary, a comprehensive approach combining logical planning, embracing growth opportunities, and enforcing reduction strategies is essential for developing Oceanview sustainably. This plan involves balancing the needs of the environment, economy, and community, ensuring long-term sustainability and resilience. |
|---|

This second answer from the GPT covers approximately the same points as the first answer from plain ChatGPT, however the points are more fleshed out and better developed.

---

## Healthcare Syste m

Now let's make the same comparison, using a healthcare system problem.

| Integrated Healthcare System Improvement Context: Imagine a medium-sized city, "Healthville," which is grappling with various healthcare challenges. The city's healthcare system is struggling to meet the growing demands of an aging population, the rise of chronic diseases, and the integration of advanced medical technologies. Additionally, Healthville needs to address disparities in healthcare access and quality among its diverse population. Challenges: Aging Population: An increasing number of elderly residents requiring specialized care and long-term support. Chronic Disease Management: A rise in chronic conditions like diabetes and heart disease, necessitating effective management and prevention strategies. Technological Integration: Incorporating new medical technologies and digital health solutions into the existing healthcare system. Access and Equity: Ensuring equitable access to healthcare services for all residents, including marginalized and low-income groups. Healthcare Workforce: Addressing shortages and ensuring the continuous training and well-being of healthcare professionals. Cost Management: Controlling rising healthcare costs while maintaining high-quality care. Objective: To develop a holistic, integrated approach to improve Healthville's healthcare system, addressing these challenges in a manner that considers the interactions between different healthcare sectors (e.g., hospitals, community care, public health) and stakeholders (e.g., healthcare providers, patients, government) . |
|---|

Initially, the unadorned ChatGPT response:

| You Solve: Integrated Healthcare System Improvement Context: Imagine a medium-sized city, … ChatGPT To improve the healthcare system in Healthville and address its complex challenges, a multi-faceted and integrated approach is needed. Here's a strategic plan: Aging Population Solutions : Develop specialized geriatric care facilities. Implement community-based support programs, like home healthcare services, to assist elderly residents. Encourage age-friendly infrastructure in healthcare facilities. Chronic Disease Management : Establish chronic disease management programs focused on lifestyle modifications, medication adherence, and regular monitoring. Integrate telehealth services for remote patient monitoring and consultation. Promote public health campaigns focused on prevention and early detection of chronic diseases. Technological Integration : Adopt electronic health records (EHR) for seamless information sharing across different healthcare providers. Invest in AI and data analytics to predict health trends and improve care delivery. Integ rate wearable health devices into patient care for real-time health monitoring. Access and Equity : Implement mobile clinics and telemedicine services to reach under-served areas. Develop policies ensuring healthcare services are affordable and accessible to all, including marginalized communities. Conduct regular community outreach to understand and address specific healthcare needs of diverse groups. Healthcare Workforce Development : Increase investment in healthcare education and training programs. Implement wellness and support programs for healthcare workers to prevent burnout. Foster a collaborative work environment across different healthcare disciplines. Cost Management : Promote the use of generic medications and cost-effective treatment options. Implement preventive healthcare measures to reduce long-term healthcare costs. Optimize resource allocation through better management systems and operational efficiencies. Collaborative and Interdisciplinary Approach : Encourage collaboration between hospitals, community care, and public health sectors. Involve stakeholders, including patients, in decision-making processes to ensure that solutions are community-centred and sustainable. Establish public-private partnerships to leverage resources and expertise from different sectors. Policy and Governance : Develop clear policies that support the integration and coordination of healthcare services. Ensure continuous evaluation and improvement of healthcare systems through data-driven methodologies. Community Engagement and Education : Conduct health education campaigns to raise awareness about preventive health, chronic disease management, and healthy lifestyles. Engage community leaders and organizations in health promotion activities. This holistic approach, which integrates care across various sectors and involves all stakeholders, aims to create a resilient, equitable, and efficient healthcare system in Healthville. |
|---|

Now the Systems Abstract Problem Solver GPT approach:

| You Solve: Integrated Healthcare System Improvement Context: Imagine a medium-sized city, "Healthville," … Systems Abstract Problem Solver Integrated Healthcare System Improvement in Healthville: Analytical Phase Logical Elements : Aging Population : Requires a systemic approach to provide specialized care and support. It's essential to analyse resource allocation and care delivery models. Chronic Disease Management : Involves understanding the current healthcare infrastructure's capacity for managing chronic diseases and identifying gaps in preventive care. Technological Integration : Focuses on assessing the current technology infrastructure and the feasibility of integrating new digital solutions. Access and Equity : Demands an examination of existing healthcare disparities and the structural reasons behind them. Healthcare Workforce : Pertains to evaluating the workforce's current state, training needs, and potential areas for improvement in staffing and skill development. Cost Management : Involves analysing current spending, funding sources, and cost-saving opportunities without compromising care quality. Energisation Elements : Aging Population : Opportunities to expand geriatric care services and long-term care facilities. Chronic Disease Management : Potential to grow preventive care programs and patient education initiatives. Technological Integration : Expanding the use of digital health tools and telemedicine services. Access and Equity : Opportunities to expand healthcare access in underserved areas and for marginalized groups. Healthcare Workforce : Expanding training programs and career development opportunities for healthcare workers. Cost Management : Identifying new funding sources and revenue models for sustainable healthcare financing. Control Elements : Aging Population : Need to reduce the burden on acute care facilities by shifting towards community-based care. Chronic Disease Management : Reducing the incidence and severity of chronic diseases through effective intervention strategies. Technological Integration : Cutting down on outdated or redundant technologies in the healthcare system. Access and Equity : Reducing disparities in healthcare access and quality. Healthcare Workforce : Decreasing staff turnover and burnout rates through effective management and support systems. Cost Management : Contracting unnecessary expenditures and optimizing resource utilization. Next, we will address each element with the appropriate ego state. You Continue. Systems Abstract Problem Solver Addressing Integrated Healthcare System Improvement in Healthville Logical Elements - Adult Ego State: Aging Population : Strategically, we need to implement a comprehensive geriatric care model that includes home-based services, assisted living facilities, and specialized geriatric wards in hospitals. The focus should be on quality of life and chronic disease management specific to the elderly. Chronic Disease Management : It's critical to establish integrated care pathways that encompass early detection, continuous monitoring, and patient education. Collaboration between primary care, specialists, and community health services is essential for a seamless patient journey. Technological Integration : Conduct a systematic evaluation of the current technological infrastructure and identify technologies that can improve efficiency and patient outcomes, like Electronic Health Records (EHRs) and telemedicine. The focus should be on interoperability and data security. Access and Equity : Undertake a thorough analysis of healthcare access across different demographics in Healthville. Implement targeted programs to address gaps, such as mobile clinics in underserved areas and language translation services. Healthcare Workforce : Develop a comprehensive workforce strategy focusing on recruitment, retention, and ongoing training. Emphasize resilience training and mental health support for staff to reduce burnout. Cost Management : Implement cost-control measures like bulk purchasing of supplies, optimizing staffing models, and utilizing technology for administrative efficiency. Explore value-based care models to align costs with patient outcomes. Energisation Elements - Child Ego State: Aging Population : Let's innovate with community engagement programs, like intergenerational activities and volunteer-led support, to enrich the lives of the elderly. Chronic Disease Management : How about gamifying health education and self-care for chronic disease patients? This could make learning and adherence more engaging and effective. Technological Integration : Let’s embrace futuristic technologies like AI for predictive analytics in disease management and VR for medical training. Access and Equity : Imagine creating community health festivals and pop-up clinics to bring healthcare directly to people in a fun and accessible way. Healthcare Workforce : We can initiate mentorship programs and innovative training simulations to make learning more dynamic and inspiring for healthcare workers. Cost Management : Let's explore new funding models, like community sponsorships or public-private partnerships, to inject more resources into the healthcare system. Control Elements - Parent Ego State: Aging Population : We must streamline the process for transitioning patients from hospital to home care or long-term care facilities to reduce hospital stay lengths. Chronic Disease Management : It's necessary to enforce strict protocols for lifestyle interventions at early stages of chronic diseases to prevent progression. Te chnological Integration : We should phase out obsolete technologies and consolidate digital tools to avoid duplication and waste. Access and Equity : Implement policies to eliminate systemic barriers in healthcare delivery, ensuring fair access for all community members. Healthcare Workforce : Enforce workload management policies to prevent staff overburdening and ensure sustainable work practices. Cost Management : Scrutinize all healthcare expenditures, eliminating non-essential spending and optimizing resource allocation. These approaches, tailored to each component of the challenge, provide a balanced and comprehensive strategy to enhance Healthville's healthcare system. |
|---|

In this case, the Systems Abstract Problem Solver GPT provided a far better explanation of the plan of action than the perfunctory ChatGPT response.

By splitting out the initial problem into the system aspects of system logic, system control, system energisation, and then addressing these areas with the ego states best suited to address each area, we were able to get a far richer and comprehensive response than was provided by unaided ChatGPT.

---

# Chapter 37. Problem Decomposition

## Real World Problems

Generally speaking, problems we encounter in everyday life can be broadly categorized into qualitative problems and quantitative problems.

- Quantitative problems involve numerical or measurable aspects and often have a straightforward, well-defined approach to finding solutions. They are about how much, how many, how often, etc.

- Qualitative problems are associated with the quality or characteristics of something rather than its quantity. They often involve subjective assessments and are typically more complex to define and solve.

In real life, many problems can have both qualitative and quantitative aspects. For example, in business, choosing a new product to develop (a qualitative problem) often goes hand in hand with budgeting and resource allocation (quantitative problems). Understanding the nature of the problem is a key step in finding the most effective solution.

Personally, we often encounter problems that are multifaceted, encompassing both quantitative (measurable, numerical) and qualitative (subjective, experiential) aspects. These complex issues require a method of deconstruction into their constituent parts to be solved correctly.

To facilitate the resolution of problems where qualitative and quantitative aspects are intertwined, then the first thing we need to do is separate these two elements so that we can treat them each appropriately.

---

## AI's Need to Decom pose Complex Problems

Scenarios where it would be useful for an automated AI system to be able to separate out the qualitative and quantitative aspects of a real-world problem include the following examples:

- Automation in Call Centre Systems : Customer enquiries are often comprised of a mix of qualitative and quantitative elements. For example, the customer may be irate that their arrived late, which is a qualitative human-centric concern, but also want their bill explained to them, which requirement is quantitative in nature.
- Automatic Code Generation Systems : In an automatic code generation system, the system must know which problems quantitative, and which problems are qualitative.

Quantitative problems can be solved using automated coding solutions since they have a finite and specific answer. Qualitative problems must be passed back to a business stakeholder user for further specification and elaboration.

- Autonomous Robotics : An AI-driven robot designed to aid in everyday tasks must be able to differentiate between quantitative and qualitative problems. For tasks that are quantitative, like measuring specific quantities of ingredients or adjusting the room temperature to a set degree, the robot can autonomously execute without external input. However, for tasks that require ethical and subjective decisions, the robot may have to rely on historical qualitative data or seeking external inputs.

In all these cases, the AI needs a predictable and reliable method of splitting out the qualitative and quantitative aspects of the original problem.

## Different Approaches to Measuring Problems

It can be very difficult to define exactly which aspects of a problem are qualitative and which aspects of a problem are quantitative.

For example:

- Customer Satisfaction Surveys : Some people measure customer satisfaction through survey scores. Other people believe that overlooks the essence of customer satisfaction and say that customer satisfaction is based on personal experiences and emotions, and cannot be simply measured.
- Social Media Engagement : Some people take a quantitative approach to social media engagement and track engagement through metrics like likes, shares, and comments. Others argue that social media engagement is not about numbers, it's about the quality of interactions and the intensity of the emotions conveyed.
- Employee Performance Evaluations : Here some people rely on metrics like sales data or project timelines to gauge employee performance objectively. Other people say that employee performance cannot be captured just by numbers; instead they stress the importance of qualitative factors such as teamwork dynamics, leadership effectiveness, and creative problem-solving.

Different people can see the same problem from different perspectives, which can lead to arguments not only in interpreting data, but also which data should be analysed in the first place.

If we want an AI to be able to address these types of complex problems, we need some way of configuring the AI to resolve problems into different elements, one way or the other.

---

## Stakeholder Consensu s Analysis

Instead of fretting about the fact that different people can see the same problem in different ways, and then wondering how we can possibly automate problem solving using AI, we can instead use exactly this disagreement to guide us in the right problem-solving approach.

- Where stakeholders agree on the nature of a problem-aspect, this indicates that this objective aspect can be defined in clear, logical terms. Subsequently, we can apply classical, clearly-defined problem solving methods to this problem element.

- On the other hand, where stakeholders disagree on the nature of a problem-aspect, this indicates that this element is subjective and so cannot be clearly defined in hard logical terms. Therefore we need to apply a "soft" problem-solving approach to this aspect of the problem.

Therefore, by recognising where agreement and disagreement lie, we can tailor our problem-solving methods accordingly. By adopting this approach, we can develop AI systems that know when to apply rigid algorithms and when to seek human qualitative input.

In other words, we can develop AI systems that are aware of their own limitations.

How would I know?, by ChatGPT

---

## Expansion of Heathrow Airport

Let's use the Stakeholder Consensus Analysis method to analyse the question of adding an extra runway to Heathrow Airport.

We'll use a GPT designed to apply Stakeholder Consensus Analysis (available at https://t.ly/b2GcK).

| You Analyse building a third runway at Heathrow Airport Stakeholder Perspective Analyser To conduct a thorough analysis of building a third runway at Heathrow Airport, we need to identify two primary stakeholders involved in this issue. In this context, typical stakeholders might include: The local community living near Heathrow Airport, which may include residents, local businesses, and local government entities. The aviation industry, including Heathrow Airport management, airlines, and associated businesses. Please confirm if these stakeholders are appropriate for this analysis or suggest alternative ones. You Use Margaret Thatcher and Michael Foot Stakeholder Perspective Analyser For an analysis involving building a third runway at Heathrow Airport with Margaret Thatcher and Michael Foot as the stakeholders, it's essential to contextualize their perspectives based on their known political and ideological standings. Although both individuals are no longer active in politics, we can infer their likely viewpoints based on their political careers and ideologies. Margaret T hatcher's Perspective (Conservative) Economic Growth and Competitiveness: Thatcher, known for her free-market policies, might view the construction of a third runway as essential for promoting economic growth, enhancing the UK's competitiveness on the global stage, and creating jobs. Infrastructure Investment: She might see it as a necessary investment in national infrastructure, aligning with her policies on modernizing the economy through strategic investments. Environmental Concerns: While environmental policies were not her administration's focus, Thatcher might weigh the economic benefits against environmental costs, possibly advocating for measures to mitigate negative environmental impacts. Michael Foot's Perspective (Labour) Environmental and Social Impact: Foot, with his strong focus on social justice and environmental protection, might oppose the runway due to potential negative impacts on local communities and the environment, emphasizing the need for sustainable development. Public Consultation: He would likely advocate for extensive public consultation and involvement in the decision-making process, ensuring that the voices of local residents and environmental groups are heard. Alternative Solutions: Foot might propose alternatives to expanding airport capacity, such as investing in public transportation or other means to reduce the need for air travel, reflecting a more environmentally friendly approach. Common Problem Elements Economic Considerations: Both Thatcher and Foot would recognize the economic implications of the third runway, though their priorities might differ (growth and competitiveness versus sustainable and equitable development). Impact on Local Communities: Both would consider the impact on local communities, albeit from different perspectives—Thatcher might focus on economic benefits, while Foot would be concerned with social and environmental justice. Unique Problem Elements Environmental Prioritization: Foot would place a higher priority on environmental concerns and sustainable development than Thatcher, who would likely prioritize economic benefits. Approach to Development: Thatcher might favour a top-down approach, emphasizing the role of the government in facilitating infrastructure projects to boost the economy. In contrast, Foot would advocate for a bottom-up approach, emphasizing public consultation and the well-being of affected communities. Recommendations For Common Elements: A classical problem-solving approach could be used to assess the economic benefits and community impact, potentially finding a middle ground that acknowledges the need for growth while ensuring local benefits and mitigating harm. For Unique Elements: Soft problem-solving approaches, including extensive stakeholder consultations and evaluations of alternative solutions, would be necessary to address the divergent views on environmental prioritization and development approaches. This analysis underscores the importance of considering diverse stakeholder perspectives in infrastructure projects, highlighting the need for comprehensive assessments that balance economic, social, and environmental factors. |
|---|

The GPT's conclusions are given to discussion, for example, even though both stakeholders raised the issue of impact on local communities, this does not necessarily mean that we can apply a hard-logic problem-solving approach to this issue.

In other words, even though both stakeholders raised the same point, but they disagreed on exactly the question of whether the impact on local communities should be addressed from an economic, measurable, perspective, or if it should be addressed from a qualitative quality-of-life perspective. Therefore it is not entirely to true to say in this case that the fact that both stakeholders mentioned the same issue indicates that we can use a hard-logic approach to solving the issue.

Nevertheless, the above example does illustrate the merits of the suggested approach, with the waiver that some fine-tuning may be needed to apply this method in practice.

---

## Stakeholder Consensus Analysis in combination with Transactional Analysis

We can apply Stakeholder Consensus Analysis in combination with Transactional Analysis by considering how different ego states would respond to the same problem.

Here too, the concept is the same as normal Stakeholder Consensus Analysis, so that we assume question elements identified by both stakeholders can be addressed using hard-logic problem solving approaches. And question elements identified by only one stakeholder must be subjective in nature and require a soft problem-solving approach.

Just that here the different stakeholders are different ego states, as opposed to different actual people.

## Waking up a Robot's Owner

Let's see if we can successfully apply Stakeholder Consensus Analysis in combination with Transactional Analysis in the following scenario:

| A robot has been instructed to wake up its owner for a meeting but knows that its owner may be in bad shape after partying late last night. |
|---|

We will use a GPT called Artificial Persona (https://t.ly/l8hRi) which is designed to follow this methodology.

| You Separate the qualitative and quantitative aspects of the following AI robot quandary: Should I wake up my owner? I know he's going to be late for his meeting if I don't, but he came home late last night and may have a hangover. I also know he wants to meet up with an old friend after his meeting. Additionally, I have access to his health data, which indicates a pattern of sleep deprivation and high stress levels lately. Artificial Person a In addressing your query, I will follow the structured process outlined in my instructions. Infer the Personality Type of the Questioner: Your question reflects a careful, analytical approach. You're considering multiple factors, suggesting a personality that values responsibility and empathy. This indicates a thoughtful, conscientious character, likely to appreciate a detailed, structured response. Generate Responses from Different Ego States: Parent Ego State: “You should wake your owner. It's your duty to ensure he's on time for his meeting. His health and well-being are important, but so are his professional responsibilities. You can gently wake him and remind him of his commitments.” Adult Ego State: “Evaluate the pros and cons. If he misses this meeting, what are the repercussions? Compare that with the potential benefits of extra sleep. Consider his recent health data, but also the importance of his work and social commitments.” Child Ego State: “Think about how he might feel. He might be grateful that you woke him up for his meeting, but he could also be upset if he's feeling unwell. Maybe find a middle ground, like letting him sleep a bit more and then waking him up.” Present Each Ego State's Perspective: The Parent perspective emphasizes responsibility and adherence to duties. The Adult perspective focuses on rational analysis and weighing consequences. The Child perspective is concerned with feelings and emotional responses. Summarize Responses: Factual (Quantitative) Information: The owner has a meeting, a planned meet-up, a pattern of sleep deprivation, and high stress levels. Experiential (Qualitative) Information: The decision to wake the owner balances professional responsibilities, health considerations, and potential emotional reactions. Research or Solve the Quantitative Aspects: The quantitative aspects here are the owner's schedule (meeting and meet-up) and his health data (sleep deprivation and stress levels). An AI robot can analyse this data to predict the likely outcomes of either waking the owner or letting him sleep. For example, calculating the minimum sleep required for health benefits versus the time needed to prepare for and reach the meeting. Conclusion: Integrating both factual and experiential insights, the most balanced approach would be to wake the owner, but with sensitivity to his potential physical state. Given the importance of both his health and his professional commitments, a gentle approach that allows for a brief assessment of his well-being upon waking would be ideal. This balances the need for sleep and health maintenance with the importance of his professional and social obligations. |
|---|

Here, the GTP's approach of mildly waking the robot's owner to further assess possible avenues of action seems like the only way to balance all the conflicting information.

---

Now let's compare that output to what we get from unadorned ChatGPT with the same query:

| You Separate the qualitative and quantitative aspects of the following AI robot quandary: Should I wake up my owner? I know he's going to be late for his meeting if I don't, but he came home late last night and may have a hangover. I also know he wants to meet up with an old friend after his meeting. Additionally, I have access to his health data, which indicates a pattern of sleep deprivation and high stress levels lately. ChatGPT The AI robot quandary about whether to wake up the owner involves both qualitative and quantitative aspects. Let's separate these: Qualitative Aspects: Ethical Considerations : Deciding whether to prioritize the owner's immediate need for rest due to a potential hangover and recent stress versus the importance of attending the meeting and meeting an old friend. Human Preferences and Well-being : Understanding the owner's preferences regarding sleep versus professional commitments and social engagements. Long-Term Health Concerns : Considering the implications of sleep deprivation and high stress on the owner's overall health and well-being. Human-AI Relationship Dynamics : Balancing the owner's trust in the AI's decision-making abilities with respecting the owner's autonomy. Quantitative Aspects: Time Constraints : Evaluating the specific time left before the meeting, and the minimum time required for the owner to prepare and arrive on time. Health Data Analysis : Quantitatively assessing patterns in the owner's health data, such as hours of sleep, stress levels, and any other relevant health metrics. Sleep Pattern Analysis : Calculating the duration and quality of the owner's sleep, especially in the context of the late return home and potential hangover. Schedule Management : Considering the timing and duration of the meeting and the planned meet-up with the friend to assess the feasibility of the day's schedule. In conclusion, the AI's decision-making process in this scenario involves a complex interplay of qualitative considerations, such as ethical dilemmas and personal preferences, and quantitative data, including time management and health metrics. Balancing these aspects is crucial for making an informed and empathetic decision. |
|---|

In this case, ChatGPT does not come to a conclusion at all.

Now what?, by ChatGPT

---

# Chapter 38. Simulating t he Human Decision-Making Process

The truth is that separating quantitative and qualitative data is what we do intuitively when faced with a multi-faceted problem. Therefore, if we ask the Artificial Persona GPT (https://t.ly/l8hRi) a real-life question, we should find that it follows the same patterns of analysis and thought that we would, in the same situation.

Let's take this GPT for a test-drive in finding ourselves a great holiday.

| You What is the best adventure holiday I can have from London on a budget of £2000? Artificial Persona To recommend an adventure holiday from London within a budget of £2000, I will apply the structured process: Infer the Personality Type of the Questioner : Based on your query, you seem to be a practical and goal-oriented individual, focused on a specific outcome within a defined budget. Generate Responses from Different Ego States : Parent Ego State: Safety and value for money are important. A holiday should be well-planned, within budget, and prioritise health and safety. Adult Ego State: Consider destinations easily accessible from London with a variety of adventure activities. Balancing cost with the quality of experience is key . Child Ego State: The holiday should be exciting and memorable. It’s a chance to explore, have fun, and experience something new and thrilling. Present Each Ego State's Perspective : Parent: Recommends choosing destinations with good healthcare facilities, safe accommodation, and reliable transport options. Advises purchasing travel insurance. Adult: Suggests researching destinations offering a balance of adventure activities (like hiking, kayaking, or cycling) and cultural experiences. Advocates for comparing costs and reading reviews. Child: Enthusiastically proposes destinations that offer unique and fun experiences, like exploring ancient ruins, snorkelling in clear waters, or experiencing local festivals. Summarise Responses : Factual (Quantitative): The holiday should be within £2000, including travel, accommodation, activities, and other expenses. Experiential (Qualitative): The destination should offer adventure, safety, and cultural richness. It should align with your desire for excitement and new experiences. Research Quantitative Aspects : I will now research destinations and adventure holiday options accessible from London within your budget. Conclusion : After the research, I'll integrate the factual findings with the experiential insights to recommend the best adventure holiday option for you. Please allow me a moment to conduct the research. Based on the structured process, here's a comprehensive analysis for an adventure holiday from London within a £2000 budget : Personality Type Inference : Your query indicates a practical, budget-conscious approach with a desire for adventure. Ego State Perspectives : Parent: Emphasises safety, value for money, and ensuring health considerations are met. Adult: Focuses on accessibility from London, variety in activities, and balancing cost with experience quality. Child: Seeks excitement, memorable experiences, and the thrill of adventure. Ego State Recommendations : Parent: Recommends destinations with robust healthcare, safe accommodations, and suggests purchasing travel insurance. Adult: Advises on researching destinations offering a mix of adventure activities and cultural experiences, ensuring they fit within the budget. Child: Desires unique and exhilarating experiences like exploring nature, engaging in local festivals, or trying new activities. Summarised Response : Factual (Quantitative): The holiday should stay within a £2000 budget, covering travel, accommodation, and activities. Experiential (Qualitative): The destination should offer adventure, safety, and cultural richness, aligning with your enthusiasm for exciting experiences . Research on Quantitative Aspects : Croatia: Offers hiking, cycling, and rafting. Ideal for exploring natural landscapes like Plitvice Lakes National Par k ​ ​ . Iceland: Known for ice-caving, glacier-hiking, and the Northern Lights. A rugged destination with dramatic landscape s ​ ​ . Cuba: Great for cyclists, offering biking, hiking, and wildlife-watching. Offers a mix of coastal beauty and cultural richnes s ​ ​ . South Africa: Ideal for safari enthusiasts. Kruger National Park is a highlight for wildlife diversit y ​ ​ . Costa Rica: Offers ziplining, hiking, surfing, and is known for its biodiversit y ​ ​ . Sri Lanka: Offers trekking, wildlife-watching, and surfing. Known for its hiking trails and rich cultur e ​ ​ . Mexico: Suitable for explorers interested in Mayan culture, hiking, and wildlife-watchin g ​ ​ . Budget Options: Responsible Travel lists several budget-friendly adventure holidays, such as a 10-day tour in Cuba from £1,54 5 ​ ​ , and a 13-day tour covering the city, forests, and beaches from £1,99 5 ​ ​ . Flights: Flight costs vary, with options from £80 return to Icelan d ​ ​ , £112 return to Jorda n ​ ​ , and £199 return to Georgi a ​ ​ . Conclusion: Considering the factual findings and experiential insights, a few standout options within your £2000 budget are: Croatia: With its diverse landscapes, it offers a mix of adventure and cultural experiences. The cost of a trip to Croatia, including flights, should fit within your budget, offering value for money and safety. Costa Rica or Mexico: Both offer rich biodiversity and cultural experiences. The total cost for either destination, including flights, is likely to be within your budget, providing an exciting and memorable holiday . Cuba: Particularly appealing if you're interested in cycling and cultural richness . The 10-day tour option fits well within your budget. These options balance the Parent's need for safety and value, the Adult's desire for a well-rounded experience within budget, and the Child's quest for adventure and new experiences. |
|---|

In the above response, we can see how the GPT has split out the qualitative and quantitative aspects of the original question, and also responded from the different TA ego states, to provide a well-researched, interesting and complete answer.

Plitvice Lakes National Park, Croatia. Wikimedia Commons

---

# Epilogue

## Using CoT Prompting Methods in Combination

The Chain of Thought Prompting methods discussed in this book of

- breaking down generative AI processing into discrete steps,

- applying the most appropriate type of thinking to solving each step, and

- recombining this thinking in a cogent manner

can be used in combination to devise powerful and transparent solving problem methodologies.

For example, in a scenario where a company is facing a complex challenge in market analysis, these techniques can be applied as follows:

- Quantitative and Qualitative Decomposition : Data is separated into numerical (sales figures, market share) and qualitative aspects (brand perception, customer satisfaction).
- Systems Analysis : The problem is further deconstructed into components like consumer behaviour, market trends, and competitor strategies.
- Psychoanalysis : Transactional Analysis is used to analyse the psychological factors influencing consumer choices and market dynamics.

At each stage, the base AI model can be accessed multiple times, providing insights specific to that element.

This sequential AI problem-solving approach allows us to use generative AI in conjunction with structured thinking techniques to achieve a broader, deeper and more transparent conclusion than is possible when using generative AI as a one-shot information processing engine.

## Programming AI

This is not a book on programming, however the following AI programming considerations come to mind after assessing the Chain of Thought Prompting methods presented in this book.

### The Intermediate Stage

The most fundamental idea that enables all programming is that we have access to intermediate stages of problem solving.

At its core, an intermediate stage in programming is a specific condition or state during the execution of a program. It can refer to the status of variables, the progress of algorithms, or the system's state at a given moment. Decisions made at intermediate stages in programming determine the direction in which a program will proceed, based on the current state or data.

The following elemental logical constructs are applied to allow decision making in intermediate program states:

- State Evaluation : The current state of a program is assessed. This could mean checking the value of variables or the status of a process.
- Decision Making : Based on the evaluation, the program makes decisions at these stages. This is where logic operations like 'if-else' statements and loops come into play. The program may choose different paths or repeat certain actions based on the conditions assessed.
- Flow Control : Intermediate stages are crucial for controlling the flow of a program. They determine what happens next in a program, whether it's proceeding to the next step, determining which information to pass to the next state, repeating a process, or terminating.

Correctly managing decision making in intermediate steps is crucial and core to all programming.

### Generative AI Intermediate States

Generative AIs, such as language models and image generators, typically function as one-shot solutions. They take input, process it through a complex network, and provide an output without exposing intermediate stages.

However, to allow a native AI programming paradigm, it's essential to be able to access the intermediate stages in the generative AI processing.

Using a structured AI thinking approach, we can break down generative AI processing into discrete stages, and access the data present in each stage, in order to make decisions about how to proceed.

- Business Process Analysis : In the case of splitting up problems into Business Process format, and then encouraging the AI to use this format to solve each part of the problem discretely, the intermediate state is presented to us as the output of each stage and the input to the next stage.

Here, we can make logical decisions based on the values of these values that are passed between each stage of the Business Process.

- Systems Analysis : When we split up problems posed to a generative AI into a systems analysis format, we can identify the states of each discrete state of the system, and make decisions based on these states.

- Transactional Analysis : In the case of using Transactional Analysis to break down the AI problem solving process into discrete parts, we have access to what each ego state, or sub-ego-state, is "thinking". This represents the intermediate state for this type of structured thinking and decisions could be made based on this information.

In each of these types of AI structured thinking, splitting the AI processing into multiple explicit steps exposes an intermediate stage which can be further analysed to make conditional decisions.

---

## Final Thought s

The advent of generative AI marks a significant shift in the landscape of information technology and creative processes. This technology is poised to transform how we approach problem-solving, creativity, and knowledge acquisition.

With generative AI, the focus shifts from the labour-intensive aspects of making IT systems function--such as coding, debugging, and system optimization--to a more strategic and holistic approach. This transition involves leveraging the capabilities of AI to handle complex, detailed tasks, freeing up human intellect for more abstract, conceptual work.

This shift enables a deeper engagement with the "bigger picture." Rather than being bogged down in the minutiae, professionals can concentrate on strategy, innovation, and high-level decision-making. This can lead to more efficient problem-solving, as the AI handles routine and repetitive tasks, allowing humans to focus on creative and analytical thinking.

By combining human creativity and strategic thinking with the efficiency and processing power of AI, we stand on the brink of a new era. This era promises not just enhanced productivity and innovation, but also the potential for significant advancements in our understanding of the world and the expansion of human knowledge.

[Imagen: Dawn | Another shot from yesterday morning. I used my 10-sto… | Flickr]

Dawn. Creator: Chris Gin

---

# Appendix A

## List of Prompt Engineering Techniques

The following is a list of generative AI optimisation techniques presented in this book.

| Prompt Engineering Technique | Description |
|---|---|
| Framing Hard Problems (page 35) | Determine the best approach for a real-world problem. |
| An Analytical GPT (page Error! Bookmark not defined. ) | Use a GPT to gain improved reasoning abilities. |
| Casting Causal Problems as a Business Process (page 65) | Solving causal problems using Business Process Analysis |
| Casting General Problems as Systems Problems (page 92) | Solving general problems using systems analysis. |
| Specifying Thinking Styles (page 119) | Ask the AI to apply a particular way of thinking when solving a problem. |
| Combining Thinking Styles (page 123) | Ask the AI to apply a combination of thinking styles when solving a problem. |
| Invoking Specific SMEs (Subject Matter Experts) (page 136) | Ask the AI to apply the expertise of specific subject matter experts when solving a problem. |
| Subject Matter Expert GPT (page 146) | Automate the process of finding and asking specific subject matter experts. |
| Performing Structural Analysis using ChatGPT (page 176) | Use ChatGPT to perform structural psychoanalysis. |
| Performing Transactional Analysis (proper) using ChatGPT (page 180) | Use ChatGPT to perform psychoanalysis of a conversation. |
| Synthesising Ego States using AI (page 193) | Simulate the responses of different ego states to a question. |
| Simulating Internal Thought (page 201) | Simulate the internal human thought processes when considering a problem from all perspectives. |
| Ego-state Specialisation in Triadic Systems Analysis (page 241) | Apply specific ego states to solving different aspects of a systems analysis problem. |
| Problem Decomposition (page 259) | Decompose real-world problems into quantitative and qualitative elements. |
| Simulating the Human Decision-Making Process (page 272) | Use a GPT to address qualitative and quantitative aspects of a real-world problem . |

---

# Appendix B

## Comparing CoT Prompting with Classical Prompt Engineering

When delving into the intricacies of CoT Prompting, it's worthwhile to take a step back and consider how classical Prompt Engineering works. This can give us a deeper appreciation of the difference between classical Prompt Engineering and CoT Prompting.

## Basic Principles of Prompt Engineering

Classical Prompt Engineering involves crafting AI prompts in a way that effectively guides the AI's algorithms to produce the required outputs. Different prompts for the same question can yield vastly different responses, even on the same AI model.

Generally speaking, we can categorise the various types of prompt engineering into the following categories.

- Widening the knowledge gap *
- Introducing counterpoints
- Demanding precision

The following sections explain each of these techniques in detail.

| * A knowledge gap is the divide between the information or understanding presented in a question and the knowledge required to answer the question effectively. This gap is also known as the epistemic gap and is a fundamental concept in epistemology, the branch of philosophy that discusses the nature and scope of knowledge . |
|---|

## Widening the Knowledge Gap

The "knowledge gap" is the disconnect that exists between the information presented within a question and the knowledge, expertise, or resources needed to provide a satisfactory response or solution.

When a question is correctly answer, the knowledge gap has been bridged. We have successfully travelled from the "question state" to the "answer state". However, when someone doesn't an answer a question properly we say, "They didn't really answer the question." This means that the answer provided didn't bridge the initial knowledge gap and therefore would not actually work if applied in practice.

In prompt engineering, we can explicitly broaden the knowledge gap presented in the question to get a more complete answer from the AI.

This means that we can rephrase the question to emphasise the breadth and depth of knowledge required for an acceptable answer, thereby demanding a thorough and elaborate response. Doing this forces the AI to generate a more comprehensive and well-considered response to our prompt.

Take for instance the simple question, "What is photosynthesis?" When asked this plain question, ChatGPT answers as follows.

| ChatGPT Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy. This process is fundamental to life on Earth, as it is the primary source of energy for nearly all living organisms. Here's a basic overview of how it works: Light Absorption : Photosynthesis starts when chlorophyll and other pigments in the plant cells absorb light (primarily sunlight). Chlorophyll is a key molecule that gives plants their green color and plays a crucial role in this process. Water Splitting and Oxygen Production : In the presence of light, water molecules ( H₂ O) in the plant cells are split into oxygen ( O ₂ ) and hydrogen ions. Oxygen is released into the atmosphere as a by-product. Carbon Dioxide Fixation : Plants take in carbon dioxide (C O₂ ) from the air through small pores in their leaves called stomata. The carbon dioxide is then used in the process of photosynthesis. Energy Conversion and Glucose Production : Using the energy absorbed from light, the plant converts the water and carbon dioxide into glucose ( C₆H ₁ ₂O₆ ), a type of sugar that plants use for energy and growth. This conversion also involves a series of complex biochemical reactions, commonly referred to as the Calvin cycle. Storage and Usage of Glucose : The glucose produced can be used immediately by the plant for energy, or it can be converted into other forms of stored energy, like starch. It can also be used to make other organic compounds necessary for plant growth and development. In summary, photosynthesis is the process by which plants use sunlight to convert water and carbon dioxide into oxygen and glucose, providing essential energy for themselves and, indirectly, for other life forms that depend on plants for food and oxygen. |
|---|

Now let's ask ChatGPT the same question again, but this time we'll widen the knowledge gap by making the gap between "the state before photosynthesis occurs" and "the state after photosynthesis occurs" more explicit.

| You How does photosynthesis convert radiative energy from the sun into potential chemical energy that is used to power all forms of life? ChatGPT Photosynthesis is a remarkable process that plants, algae, and certain bacteria use to convert solar energy into chemical energy, which is fundamental for sustaining almost all life on Earth. Here's a simplified overview of how this process works: Absorption of Sunlight : Photosynthesis begins in the cells of plants and algae, specifically within organelles called chloroplasts. These chloroplasts contain pigments, primarily chlorophyll, which absorb sunlight. Different pigments absorb different wavelengths of light, but chlorophyll mainly absorbs blue and red light, reflecting green light, which is why plants appear green. Light-Dependent Reactions : Once the light is absorbed, it excites electrons in the chlorophyll. This energy from the excited electrons is used to split water molecules ( H₂ O) into oxygen ( O₂ ) and hydrogen ions ( H⁺ ). The oxygen is released into the atmosphere, which is crucial for the air we breathe. The energy captured is also used to create adenosine triphosphate (ATP) and nicotinamide adenine dinucleotide phosphate (NADPH), which are energy-carrying molecules. Light-Independent Reactions (Calvin Cycle) : This stage doesn't require light directly and takes place in the stroma of the chloroplasts. Here, the energy stored in ATP and NADPH is used to fix carbon dioxide (C O₂ ) from the atmosphere. Through a series of reactions known as the Calvin Cycle, C O₂ is combined with a five-carbon sugar (ribulose bisphosphate) to produce glucose ( C₆H ₁ ₂O₆ ), which is a simple sugar. Formation of Glucose and Oxygen : The end products of photosynthesis are glucose and oxygen. Glucose is a form of chemical energy that can be used by the plant for growth, reproduction, and other life processes. Oxygen, a byproduct, is released into the atmosphere. In essence, photosynthesis transforms the radiant energy of the sun into potential chemical energy in the form of glucose. This process is crucial because it provides the primary energy source for nearly all living organisms either directly (for herbivores) or indirectly (for carnivores). Moreover, photosynthesis is responsible for producing and maintaining th e oxygen content of the Earth's atmosphere, making life as we know it possible. |
|---|

By explicitly asking ChatGPT how to bridge the pre-photosynthesis state to the post-photosynthesis state, we have persuaded ChatGPT to provide far more detail in its answer.

You could object however, that without prior knowledge we wouldn't have been able to "widen the knowledge gap" in this way, since we had to know how to phrase the question correctly in the first place.

To address this issue, we can ask ChatGPT to widen the knowledge gap by itself, and only then proceed to answer the question.

| You Widen the knowledge gap in the following question and then answer it: What is photosynthesis? ChatGPT The widened question would be: "How does the process of photosynthesis in plants convert solar energy into chemical energy, and what are the roles of chlorophyll, carbon dioxide, water, and light in this process?" Photosynthesis is a complex biochemical process that plants, algae, and some bacteria use to convert solar energy into chemical energy. This energy is stored in the bonds of sugar molecules, which are later used by the organism as a source of energy. The process primarily occurs in the chloroplasts of plant cells, where chlorophyll, a green pigment, plays a critical role. The process of photosynthesis can be broadly divided into two stages: the light-dependent reactions and the light-independent reactions (Calvin cycle). Light-Dependent Reactions : These reactions occur in the thylakoid membranes of the chloroplasts and require light. When sunlight strikes the chlorophyll molecules, it excites the electron s within these molecules, leading to a series of reactions that generate ATP (adenosine triphosphate) and NADPH (nicotinamide adenine dinucleotide phosphate). These are energy-carrying molecules that store the energy harnessed from sunlight. Water molecules are also split in this process, releasing oxygen as a byproduct. Light-Independent Reactions (Calvin Cycle) : These reactions occur in the stroma of the chloroplasts and do not require light directly. Instead, they use the ATP and NADPH produced in the light-dependent reactions to convert carbon dioxide from the atmosphere into glucose, a simple sugar. This process involves a series of enzymatic reactions where the carbon dioxide is fixed (i.e., incorporated into organic molecules). In summary, photosynthesis is essential for life on Earth as it provides the primary means of producing organic compounds from inorganic substances, using light as the energy source. This process not only fuels the organisms that perform photosynthesis but also provides oxygen and organic compounds that are crucial for other organisms, including humans. |
|---|

In this case, ChatGPT itself first widened the knowledge gap in our simple question, and then gave a more comprehensive answer.

## Counterpoints

Using counterpoints in prompt engineering means that we include contrasting perspectives within a prompt. This stimulates the AI to apply critical thinking forces it to provide a more balanced response.

Counterpoints can be introduced by playing devil's advocate or by incorporating opposing viewpoints. By challenging the AI to consider multiple angles and underlying complexities, the AI's answers become more comprehensive and include a higher level of critical thinking.

For example, let's first ask ChatGPT a plain question, without a counterpoint.

| You Explain the benefits of renewable energy. ChatGPT Renewable energy, which includes sources like solar, wind, hydroelectric, and geothermal power, offers several significant benefits compared to traditional fossil fuels: Environmental Protection : Renewable energy sources generate far less pollution and greenhouse gases than fossil fuels. This reduction in air and water pollution is crucial for combating climate change and protecting ecosystems and biodiversity. Sustainable and Inexhaustible : Unlike fossil fuels, which are finite, renewable energy sources are virtually inexhaustible. The sun will continue to shine, the wind will keep blowing, and rivers will flow for billions of years, making these energy sources sustainable for the long-term future. Reduced Greenhouse Gas Emissions : Burning fossil fuels is a major contributor to greenhouse gas emissions, notably carbon dioxide and methane. Renewable energy sources produce minimal greenhouse gases, helping to mitigate climate change. Energy Independence and Security : Countries can reduce their dependence on imported fuels by developing renewable energy resources. This enhances energy security and can protect nations from price fluctuations in global energy markets. Economic Development and Job Creation : The renewable energy sector is labour-intensive, which means it creates a lot of jobs. These range from manufacturing and installation to maintenance and engineering, contributing to economic growth. Decrease in Health Risks : By reducing air pollution, renewable energy sources can lead to a decrease in health problems caused by pollutants from fossil fuels. This can result in fewer health-related expenses and improved overall public health. Technological Innovation and Cost Reduction : As technology in renewable energy advances, the cost of these technologies drops. Solar panels and wind turbines have become significantly cheaper over the past decade, making renewable energy more competitive with fossil fuels. Energy Accessibility : Renewable energy technologies can be deployed in remote and rural areas where it's not economically viable to extend the traditional power grid. This can improve access to energy in developing countries or remote locations. Flexibility and Scalability : Many forms of renewable energy, particularly solar and wind, can be scaled to fit a variety of needs, from small personal devices to large power plants. Conservation of Water Resources : Traditional power generation methods often require large amounts of water for cooling. Most renewable energy sources use significantly less water, helping to conserve this vital resource. In summary, renewable energy offers a sustainable, environmentally friendly, and economically beneficial alternative to fossil fuels, playing a crucial role in combating climate change, improving public health, and ensuring a more secure and independent energy future. |
|---|

In this case, ChatGPT's response is straightforward and only focuses on positive aspects, as prompted. Now let's ask the same question again, but this we'll ask ChatGPT to take counterpoints into account.

| You Explain the benefits of renewable energy, taking counterpoints into account. ChatGPT Renewable energy, derived from natural processes that are continuously replenished, includes sources like solar, wind, hydro, geothermal, and biomass. It offers several benefits, but also faces some challenges and counterpoints. Benefits of Renewable Energy Environmental Impact : Renewable energy sources produce little to no greenhouse gas emissions during operation, making them cleaner and safer for the environment compared to fossil fuels, which release carbon dioxide and other harmful pollutants. Sustainability : As renewables are based on natural resources that are either inexhaustible or can be replenished quickly (like wind, sun, and water), they offer a more sustainable energy solution than fossil fuels, which are finite. Energy Security : Using renewable sources can reduce dependence on imported fuels, enhancing energy security for many countries and reducing the risks associated with fuel supply disruptions. Economic Benefits : The renewable energy sector can create jobs in manufacturing, installation, and maintenance. It also often involves local materials and labour, which can boost local economies. Health Benefits : By reducing air pollution, renewables contribute to better health outcomes. The decrease in pollutants like sulphur dioxide and particulate matter can lead to fewer respiratory and cardiovascular diseases. Counterpoints and Challenges Intermittency and Reliability : Many renewable sources like solar and wind are intermittent, meaning they don't produce energy all the time. This can lead to reliability issues for the power grid, requiring backup systems or storage solutions. Energy Storage Costs : To address intermittency, energy storage systems (like batteries) are needed, but these can be expensive and are still in the developmental stage for large-scale appli cations. Initial Investment : The upfront cost for renewable energy technologies can be higher than traditional fossil fuels. While the long-term operating costs may be lower, the initial investment is a barrier for many. Environmental Impact of Production : While operating emissions are low, manufacturing renewable energy systems (like solar panels and wind turbines) does have an environmental impact, including the use of raw materials and energy. Land Use : Certain renewable energy projects, especially wind farms and large solar installations, require significant land use, which can lead to habitat loss and other environmental concerns. Technological Maturity : Some renewable technologies, especially newer ones, are not yet as technologically mature or efficient as fossil fuel technologies, which have been developed and refined over a longer period. In conclusion, while renewable energy presents a promising path towards a more sustainable and environmentally friendly future, it is important to address the accompanying challenges through technological innovations, policy support, and infrastructure development. Balancing the benefits and drawbacks is crucial in the transition to a cleaner energy future. |
|---|

This time, including counterpoints makes ChatGPT provide a nuanced and realistic understanding of the subject matter.

The balanced narrative includes a deeper analytical approach and a comprehensive grasp of the topic, which is the result of considering diverse viewpoints in the analysis.

## Demanding Precision

The basis of providing a good answer is to precisely define what is being said in answer to the question. If we do not express ourselves clearly then we could mean the right thing, but nobody will ever know that.

Demanding precision from an AI requires a precise and clear formulation of both the question and the expected answer. The following table lists various prompt engineering strategies for ensuring precision in the AI's response.

| Technique | Explanation |
|---|---|
| Detail-Oriented Queries | The precision of an AI’s response is directly influenced by the specificity of the query. For example, instead of asking "How do electric cars work?" we can ask "Explain which components function together to ensure the correct functioning of electric vehicles." |
| Set Contextual Boundaries | Clearly delineating the scope of the question avoids broad, generalised answers. For instance, instead of generally asking about the impact of renewable energy on the UK, we can ask, “How must the UK energy infrastructure be updated to manage renewable energy sources.” |
| Ask for Definitions | Request specific definitions of terms or concepts. For example, instead of asking, "What is machine learning?" we can ask, "Can you define supervised and unsupervised machine learning, highlighting their differences?" |
| Request Examples | Ask for examples to illustrate a point. For instance, "Provide three specific examples of how blockchain technology is being used in finance." |
| Clarify Scenarios | Specify the scenario being asked about. For example, instead of “What are the current cybersecurity best practices?” we can ask "In the scenario of a data breach, what specific steps should a company follow according to current cybersecurity best practices?". |
| Compare and Contrast | Ask the AI to compare and contrast ideas. For example, instead of asking, “Are electric cars good for the environment?” we can ask "In terms of environmental impact, how do electric cars compare to petrol-powered cars?" |

In addition to the above techniques, we can simply directly ask the AI to be precise in its answer.  For example, compare the two following response from ChatGPT:

| You I have a persistent cough and a high fever. What might be wrong with me? ChatGPT I'm not a doctor, but a persistent cough and a high fever could be symptoms of various illnesses ranging from a common cold to more serious conditions like influenza, pneumonia, or even COVID-19. These symptoms can also be associated with other respiratory infections or conditions. Given these symptoms, it's important to consult with a healthcare professional for an accurate diagnosis and appropriate treatment. They might recommend rest, fluids, and over-the-counter medication to manage the symptoms, but a medical evaluation is crucial, especially if your symptoms are severe or persistent. In the meantime, it's advisable to rest, stay hydrated, and monitor your symptoms. If you experience difficulty breathing, persistent pain or pressure in the chest, new confusion, inability to wake or stay awake, or bluish lips or face, seek medical attention immediately, as these could be signs of a more serious condition. |
|---|

With:

| You I have a persistent cough and a high fever. What might be wrong with me? Be precise and rigorous. ChatGPT I'm not a doctor, but based on your symptoms of a persistent cough and high fever, there are several possible causes. However, it's important to remember that only a healthcare professional can provide a definitive diagnosis after a thorough examination. Here are some common conditions that might present with these symptoms: Influenza (Flu) : A viral infection affecting the respiratory system. Symptoms often include a high fever, cough, body aches, and fatigue. Common Cold : Typically less severe than the flu, but can still cause a cough and low-grade fever. COVID-19 : Caused by the coronavirus SARS-CoV-2, it often presents with a fever, cough, and sometimes shortness of breath, among other symptoms. Pneumonia : An infection of the lungs that can be caused by bacteria, viruses, or fungi. Symptoms often include a high fever, cough (which may produce phlegm), and chest pain. Bronchitis : Inflammation of the bronchial tubes, which carry air to your lungs. It often results in a cough that may bring up mucus, as well as a low fever. Tuberculosis : A bacterial infection that mainly affects the lungs. Symptoms include a persistent cough (sometimes with blood), fever, night sweats, and weight loss. Whooping Cough (Pertussis) : A highly contagious respiratory tract infection marked by a severe hacking cough followed by a high-pitched intake of breath that sounds like "whoop." Given the variety of potential causes, some of which are quite serious, it's very important to consult with a healthcare provider for a proper diagnosis and treatment plan. They may recommend diagnostic tests like blood tests, chest X-ray, or a throat swab depending on your specific symptoms and medical history. |
|---|

Simply by asking ChatGPT to be precise, it gave a more precise answer.
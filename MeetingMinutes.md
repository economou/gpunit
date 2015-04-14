# Meeting Dates #


# 5/2/11 #
> - Feedback on presentation from advisor meeting:
  * Add logo + website URL to presentation.
  * Replace Starlab pic w/image of important experiment (from Steve's work).
  * AMUSE website URL, acknowledge AMUSE developers.
  * Picture of AMUSE's Python source code on slide about State of AMUSE.
  * Picture of something gpunit-related (small GUI image contrasting with python code pictures) on the "Purpose" slide.
  * Picture of telescope or something on "Target Audience" slide.
  * Picture of architecture diagram on the "Components/Features" slide.
  * Add "easy cluster access" to features/design page. Picture of cluster on that page, picture of GPU. Combine those two slides.
  * Change order of modules and node viewer slides.
  * Move testing after team management, add Gantt chart on team management page.
  * Mention how 2x-week team meetings made our progress better.
  * Spent time learning domain a lot first, waterfall design except in the beginning we couldn't plan completely.
  * Things we learned in dev process.
  * Put case studies back in.
  * Don't try to make AMUSE sound bad, is a huge step forward over separated FORTRAN modules etc...
  * Would've saved Tim time had we had out project out when he started.
  * Demo it to Steve soon.
  * Ask Steve about what Obs. Astrophysicists do.
  * Meet next week for dry run Monday at 5PM.
  * Send and update on slides BEFORE next weekend.

# 4/18/11 #
  * Demonstrated beta prototype
    * Custom Particles
    * Experiment/Module XML
    * OpenGL Diagnostic Window
  * Work for next meeting (5/2/11):
    * Complete more features (see project plan)
    * Run user testing (Tim, maybe Prof. McMillan)
    * Get feedback and implement changes accordingly.
    * **Final Presentation Draft**

# 4/13/11 #
  * Met to work on some code as a group, answered implementation questions.

> - Attendance: Andrew, Gabe, Jason, Raj, Tim

# 4/11/11 #
  * Checked progress.
  * Gabe demonstrated some GUI toolkit features.
  * Planned to meet Wednesday.

> - Attendance: Andrew, Gabe, Jason, Raj, Tim

# 4/6/11 #
> - Confirmed assignments of work for the beta prototype.
    * Andrew/Jason: Get a full implementation of a wrapper for Hermite0 (basic gravity module) working.
    * Dan: Add some more diagnostics beyond the basics.
    * Tim: Implement an experiment (hand written) using our Module/Experiment wrapper classes.
    * Raj: Logging
    * Gabe: Implement functionality of GUI, interaction with wrapper classes and network.

> - Attendance: All.

# 4/4/11 #
> - Discussed plans for the coming weeks.
    * By 4/18: Some form of working prototype w/GUI, can run an experiment.
    * By 5/2: Update prototype, obtain user feedback after first prototype and make fixes.
    * Rough draft of presentation.
    * By 5/9: Dry run of presentation.

> - Presentation needs some form of visualization so that we can show something interesting (not just raw data or graphs).

> - Attendance: Gabe, Tim

# 3/2/11 #

Assigned work for next week (by Wednesday). Tasks are:
  * Gabe: GUI -> pyQt4, network implementation
  * Andrew/Jason: Initial conditions class + integration with experiment
  * Raj: Implement logging classes from SDD
  * Tim: get the AMUSE script working with at least one module
  * Dan: Implement some basic diagnostics from Alf's samples.

# 2/21/11 #
  * Received feedback on design presentation, more design comments.

  * "Code generation" -> experiment generation
  * "Interface" -> experiment design
  * Networking: don't explicitly rely on AMUSE or MPI, let the design just require that there be some "glue" to connect modules and running experiments to each other.
  * Generated code must be human-readable so that users can modify it (new requirement)

  * In general things should be more decoupled.

# 2/14/11 #
  * Received design document feedback.
  * Design document should define some experiment result structure.
  * Move code generation into a separate module.
  * Use cases should be the prime motivation behind testing.

  * Selenium for automated GUI testing.

# 11/08/10 #
  * 5:10 Meeting start.

  * 5:10 Discussion of UseCases
    * Different Types of Posisble actors (Basic, Intermediate, Advanced)

  * 5:17 Presentation
    * What needs to be talked about during the presentation.
    * A few images of what the GUI will look like
    * Discussion of what all of the Diagnostic tools will be
    * The slides will be a summary of what is on the document

  * 5:30
    * Work on more defined glossary items.

  * 5:40
    * Todo list:  Till Friday look over the SRS
    * Jason and Tim will be working on the Use cases

  * Priority 1 Logging for viewing the experiment.
    * Add to Requirement Document about Logging, Diagnostic, Intermediate Diagnostics output.

  * Tim needs to Email Alf about the Diagnostic Code, then we will splitting code up between everyone so we aren't overwhelmed

# 11/02/10 #
  * ### Requirements Document Draft Review ###
    * Use present tense throughout
    * Don't refer to the product as a "GUI"
      * We need to define what the product IS
        * "ProductName is X, Y, Z; and a GUI facilitating A, B, and C."
    * Use Cases will be the meat of the document
      * See the ad-hoc network project doc for good examples
      * Show how someone would go through the steps of doing X with the product (where X is creating something, etc.)
    * Include Activity Diagrams
      * "Here's what the user wants to accomplish; these are the steps involved in accomplishing that."
      * Follow the standard for such diagrams.
    * GUI prototypes
      * Make elements larger in document; zoom in on different areas of the GUI if necessary
      * Include text explanation of the basic GUI regions/elements
  * ### Miscellaneous ###
    * It's OK to change the group name
    * Group name should ideally match product name

# 10/26/10 #
  * Decided we are going to be creating a GUI.
  * Discussed an overall hierarchy of what each section will look like for the Requirement Documentation.
  * Decided who is doing what, listed in the Notes section.
  * Discuss Deadlines: By the time we are done with our meeting at 6pm on Monday we will be Done our rough draft.
  * ## Notes ##
    * Introduction - Describe Amuse and discuss how it will be implimented with a GUI.  Describe Problem or Need and how it will be addressed. Discuss on how we have to write a Python script.
    * Glossary
    * Functional Requirements - What the user will be able to do with Scripts.  What the requirements are to be able to interact with lower modules.  (Need a firm idea on what the GUI elements will be)
    * Use Cases - Snapshots of our GUI. User needs to be able to do this.
    * Non-Functional Requirments
    * System Evolution - Where is this going to go. What is the future of this. (Do not need to have a business plan but should have some kind of explanation of how it is going to be used.)
    * ### Requirements Document Assignees ###
      * Gabe - GUI Prototyping
      * Jason  - Use Cases
      * Raj    - System Evolution, Glossary
      * Dan    - Functional Requirement
      * Tim    - Introduction
      * Andrew - Non-Functional Requirements
  * ## TODO ##
    * We want to get Alf to come to the next meeting on November 1st, 4:30 to 6pm, or 5-6 on Tuesday.
  * ## Attendance ##
    * Everyone

# 10/19/10 #
  * Discussed potential project options and strategies for implementation.
    * Settled on the GUI option: GUI will allow user to put modules together, provide input data and run the experiment.
    * Some short discussion on what we'd use to implement it (languages, GUI toolkits etc...)
  * ## TODO ##
    * Learn more about AMUSE, hopefully have Alf demo it for us with a small experiment.
    * Requirements Document + Abstract + Project Plan: Need to figure out what the GUI will do, functionality etc. Need to think of use cases and what the GUI will look like (very basic drawings etc...).
    * How will the user interact with our environment (command line would be important).
    * How does our project communicate with AMUSE?

  * ## Attendance ##
    * Everyone

# 10/18/10 #
  * Met with Prof. McMillan to discuss potential directions for the project.
  * Exchanged prior experience info for group members.
  * Project options:
    * GUI to tie modules together.
    * Parallelization layer for dividing up work.
    * Parallel algorithms (probably not a good main project)

  * ## Attendance ##
    * Everyone
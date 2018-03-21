[Markdown]: http://daringfireball.net/projects/markdown/
[reveal.js]: http://github.com/hakimel/reveal.js

# TJSlids
### Text based slides generator.
Usage Guide

## What is TJSlides
TJSlides is a text based slides generator.  
Edit text in [Markdown],  
and translate into [reveal.js] supported format.

### That is
You have to know  
some [Markdown] syntax  
to use TJSlides.

## How it paginates?
There are 6 headings in [Markdown]:

    # Heading 1
    ## Heading 2
    ### Heading 3
    #### Heading 4
    ##### Heading 5
    ###### Heading 6

Syntax `#` and `##` was used for paginating.  
Generally,  
`#` is for start page's title,  
while `##` is for common page's title.

## Heading Example
    ## Heading 2
### Heading 3
    ### Heading 3
#### Heading 4
    #### Heading 4
##### Heading 5
    ##### Heading 5
###### Heading 6
    ###### Heading 6

## Unordered List
*   one
*   two
*   three

---

    *   one
    *   two
    *   three

## Ordered List
1.  One
2.  Two
3.  Three

---

    1.  One
    2.  Two
    3.  Three

## QUOTES
> Our destiny offers not the cup of despair,
> but the chalice of opportunity. So let us seize it,
> not in fear, but in gladness.

by R.M. Nixon

## Links
### There are two ways:
[Inline](http://tjslides.herokuapp.com):

    [Inline](http://tjslides.herokuapp.com):

[Reference-style][id] (titles are optional):
[id]: http://tjslides.herokuapp.com "Title"

    Reference-style [labels][id] (titles are optional):
    Then, anywhere else in the doc, define the link:
    [id]: http://tjslides.herokuapp.com "Title"

## Images
Just like links but a exclamation point prepend.

![Tony Jian](http://i.imgur.com/ShxGX.jpg "Tony Jian")

Inline (titles are optional):

    ![Tony Jian](http://i.imgur.com/ShxGX.jpg "Tony Jian")

Reference-style:
    [id]: http://tonytonyjan.github.com/images/ice-ball.jpg "Title"

## Preformatted Code Blocks
Indent every line of a code block by at least 4 spaces or 1 tab.
This is a normal paragraph.

    class Fixnum
      def prime?
        ('1' * self) !~ /^1?$|^(11+?)\1+$/
      end
    end

---

    Indent every line of a code block by at least 4 spaces or 1 tab.
    This is a normal paragraph.
    
        class Fixnum
          def prime?
            ('1' * self) !~ /^1?$|^(11+?)\1+$/
          end
        end

# Courtesy of reveal.js
 
## Holistic Overview
Press **ESC** to enter the slide overview!

## Works in Mobile Safari
You can swipe through the slides pinch your way to the overview.

## Interconnections
You can link between slides internally,  
[like this.](#/3)

    You can link between slides internally,  
    [like this.](#/3)

# THE END
### <a href="/users/sign_in" target="_top">Sign in!</a> and <a href="/slides/new" target="_top">Try it now!</a>

This is a module that allows to add a field to views that would allow users to choose among all possible emails (from different models) one may want to specify in a field.
For example, one may want to choose both an email of a department from the module hr.department (which doesn't originally contain a field for email, but it's a reasonable place to add such field to) and emails of some res.partners, too, so that a mail is sent both to a department's mail and to some res.partner's mails, that were all chosen in a single field.


# Example
Let's now add a field to Time Off model connected to 'res.email' model defined in this module:
![image](https://user-images.githubusercontent.com/100222271/209962176-8cf8b055-f296-4abd-857d-3f4e72de8456.png)

Now let's add this new field to a time off form view to see it working:
![image](https://user-images.githubusercontent.com/100222271/209962692-72c7f7c3-42fa-4eb8-a475-b49e3e0dc439.png)

![image](https://user-images.githubusercontent.com/100222271/209962378-08939133-c813-4477-a5f0-724b4d350c9a.png)

As you can see, you can now pick different entities there:
![image](https://user-images.githubusercontent.com/100222271/209962997-966c978d-a0fe-4d93-ada5-66a8fced3d36.png)

And each of them has emails associated with them. Here you can see how the essential information is stored in the database. Note that the 'name' (which is the representation of those fields in the dropdown we saw above) is not stored, hence NULL values:
![image](https://user-images.githubusercontent.com/100222271/209963425-f8c348d0-f613-4660-a618-0df1cecb1203.png)

Now you can write some custom logic that would send notifications to the emails of those entities.

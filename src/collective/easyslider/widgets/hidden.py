# from z3c.form.interfaces import ITextWidget
# from z3c.form.browser.text import TextWidget
# from zope.interface import implementer, implementer_only
# import z3c.form.widget


# @implementer_only(ITextWidget)
# class HiddenWidget(TextWidget):

#     def render(self):
#         import pdb; pdb.set_trace()  # NOQA: E702
#         return self.hidden()

# @implementer(z3c.form.interfaces.IFieldWidget)
# def HiddenFieldWidget(field, request):
#     return z3c.form.widget.FieldWidget(field, HiddenWidget(request))

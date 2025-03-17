from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class CategoriaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    preco = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

class MovimentacaoForm(FlaskForm):
    produto_id = SelectField('Produto', coerce=int, validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('saida', 'Saída')], validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    observacao = TextAreaField('Observação', validators=[Optional()])
    submit = SubmitField('Registrar') 
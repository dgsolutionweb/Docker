import os
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate

from config import Config
from models.models import db, Produto, Categoria, Movimentacao
from models.forms import ProdutoForm, CategoriaForm, MovimentacaoForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    total_produtos = Produto.query.count()
    total_categorias = Categoria.query.count()
    total_movimentacoes = Movimentacao.query.count()
    
    # Produtos com estoque baixo (menos que 10 unidades)
    produtos_estoque_baixo = Produto.query.filter(Produto.quantidade < 10).order_by(Produto.quantidade).limit(5).all()
    
    # Últimas movimentações
    ultimas_movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).limit(5).all()
    
    return render_template('index.html', 
                           total_produtos=total_produtos,
                           total_categorias=total_categorias,
                           total_movimentacoes=total_movimentacoes,
                           produtos_estoque_baixo=produtos_estoque_baixo,
                           ultimas_movimentacoes=ultimas_movimentacoes)

# Rotas para Produtos
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    form = ProdutoForm()
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            quantidade=form.quantidade.data,
            categoria_id=form.categoria_id.data
        )
        db.session.add(produto)
        db.session.commit()
        
        # Registra entrada inicial do produto no estoque
        if form.quantidade.data > 0:
            movimentacao = Movimentacao(
                produto_id=produto.id,
                tipo='entrada',
                quantidade=form.quantidade.data,
                observacao='Entrada inicial'
            )
            db.session.add(movimentacao)
            db.session.commit()
            
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    
    return render_template('produto_form.html', form=form, produto=None)

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        # Verifica se a quantidade mudou para registrar movimentação
        qtd_anterior = produto.quantidade
        
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.categoria_id = form.categoria_id.data
        
        # Só atualiza a quantidade se houve movimentação
        if qtd_anterior != form.quantidade.data:
            diferenca = form.quantidade.data - qtd_anterior
            
            # Registra movimentação
            tipo = 'entrada' if diferenca > 0 else 'saida'
            movimentacao = Movimentacao(
                produto_id=produto.id,
                tipo=tipo,
                quantidade=abs(diferenca),
                observacao=f'Ajuste manual de estoque'
            )
            db.session.add(movimentacao)
            
            # Atualiza quantidade do produto
            produto.quantidade = form.quantidade.data
            
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    
    return render_template('produto_form.html', form=form, produto=produto)

@app.route('/produtos/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    
    # Primeiro exclui as movimentações relacionadas ao produto
    Movimentacao.query.filter_by(produto_id=id).delete()
    
    db.session.delete(produto)
    db.session.commit()
    
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('listar_produtos'))

@app.route('/produtos/movimentar/<int:id>', methods=['GET', 'POST'])
def movimentar_produto(id):
    produto = Produto.query.get_or_404(id)
    form = MovimentacaoForm()
    form.produto_id.choices = [(produto.id, produto.nome)]
    form.produto_id.data = produto.id
    
    if form.validate_on_submit():
        quantidade = form.quantidade.data
        tipo = form.tipo.data
        
        # Valida se há estoque suficiente para saída
        if tipo == 'saida' and quantidade > produto.quantidade:
            flash(f'Quantidade insuficiente em estoque! Disponível: {produto.quantidade}', 'danger')
            return render_template('movimentacao_form.html', form=form, produto=produto)
        
        movimentacao = Movimentacao(
            produto_id=produto.id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=form.observacao.data
        )
        
        # Atualiza o estoque do produto
        if tipo == 'entrada':
            produto.quantidade += quantidade
        else:
            produto.quantidade -= quantidade
            
        db.session.add(movimentacao)
        db.session.commit()
        
        flash('Movimentação registrada com sucesso!', 'success')
        return redirect(url_for('listar_movimentacoes'))
    
    return render_template('movimentacao_form.html', form=form, produto=produto)

# Rotas para Categorias
@app.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/nova', methods=['GET', 'POST'])
def nova_categoria():
    form = CategoriaForm()
    
    if form.validate_on_submit():
        categoria = Categoria(nome=form.nome.data)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('listar_categorias'))
    
    return render_template('categoria_form.html', form=form, categoria=None)

@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)
    
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('listar_categorias'))
    
    return render_template('categoria_form.html', form=form, categoria=categoria)

@app.route('/categorias/excluir/<int:id>')
def excluir_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    
    # Não excluímos os produtos, apenas desvinculamos da categoria
    for produto in categoria.produtos:
        produto.categoria_id = None
    
    db.session.delete(categoria)
    db.session.commit()
    
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('listar_categorias'))

# Rotas para Movimentações
@app.route('/movimentacoes')
def listar_movimentacoes():
    # Filtros
    tipo = request.args.get('tipo')
    produto_id = request.args.get('produto_id', type=int)
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Query base
    query = Movimentacao.query
    
    # Aplicando filtros
    if tipo:
        query = query.filter(Movimentacao.tipo == tipo)
    
    if produto_id:
        query = query.filter(Movimentacao.produto_id == produto_id)
    
    if data_inicio:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
        query = query.filter(Movimentacao.data >= data_inicio_obj)
    
    if data_fim:
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(Movimentacao.data < data_fim_obj)
    
    # Ordenando
    movimentacoes = query.order_by(Movimentacao.data.desc()).all()
    
    # Lista de produtos para o filtro
    produtos = Produto.query.all()
    
    return render_template('movimentacoes.html', movimentacoes=movimentacoes, produtos=produtos)

@app.route('/movimentacoes/nova', methods=['GET', 'POST'])
def nova_movimentacao():
    form = MovimentacaoForm()
    form.produto_id.choices = [(p.id, p.nome) for p in Produto.query.all()]
    
    if form.validate_on_submit():
        produto_id = form.produto_id.data
        quantidade = form.quantidade.data
        tipo = form.tipo.data
        
        produto = Produto.query.get(produto_id)
        
        # Valida se há estoque suficiente para saída
        if tipo == 'saida' and quantidade > produto.quantidade:
            flash(f'Quantidade insuficiente em estoque! Disponível: {produto.quantidade}', 'danger')
            return render_template('movimentacao_form.html', form=form)
        
        movimentacao = Movimentacao(
            produto_id=produto_id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=form.observacao.data
        )
        
        # Atualiza o estoque do produto
        if tipo == 'entrada':
            produto.quantidade += quantidade
        else:
            produto.quantidade -= quantidade
            
        db.session.add(movimentacao)
        db.session.commit()
        
        flash('Movimentação registrada com sucesso!', 'success')
        return redirect(url_for('listar_movimentacoes'))
    
    return render_template('movimentacao_form.html', form=form)

@app.template_filter('now')
def now_filter(format_type=''):
    if format_type == 'year':
        return datetime.now().year
    return datetime.now()

# Inicialização do banco de dados
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Verifica se já existem categorias, senão cria algumas padrão
    if Categoria.query.count() == 0:
        categorias = [
            Categoria(nome='Alimentos'),
            Categoria(nome='Bebidas'),
            Categoria(nome='Limpeza'),
            Categoria(nome='Papelaria'),
            Categoria(nome='Eletrônicos')
        ]
        db.session.add_all(categorias)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 
"""Initial migration after cleanup

Revision ID: 45542333b0ab
Revises: 
Create Date: 2024-07-31 23:32:10.638028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '45542333b0ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faqs',
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faqs_id'), 'faqs', ['id'], unique=False)
    op.create_table('product_categories',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_product_categories_id'), 'product_categories', ['id'], unique=False)
    op.create_table('topics',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_topics_id'), 'topics', ['id'], unique=False)
    op.create_table('newsletter_subscribers',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('newsletter_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['newsletter_id'], ['newsletters.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', 'newsletter_id', name='uq_subscriber_newsletter')
    )
    op.create_index(op.f('ix_newsletter_subscribers_id'), 'newsletter_subscribers', ['id'], unique=False)
    op.create_table('notification_settings',
    sa.Column('mobile_push_notifications', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('email_notification_activity_in_workspace', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('email_notification_always_send_email_notifications', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('email_notification_email_digest', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('email_notification_announcement_and_update_emails', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('slack_notifications_activity_on_your_workspace', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('slack_notifications_always_send_email_notifications', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('slack_notifications_announcement_and_update_emails', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_settings_id'), 'notification_settings', ['id'], unique=False)
    op.create_table('product_variants',
    sa.Column('size', sa.String(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=True),
    sa.Column('product_id', sa.String(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_variants_id'), 'product_variants', ['id'], unique=False)
    op.drop_table('user_newsletter_association')
    op.add_column('billing_plans', sa.Column('duration', sa.String(), nullable=False))
    op.add_column('billing_plans', sa.Column('description', sa.String(), nullable=True))
    op.add_column('newsletters', sa.Column('description', sa.Text(), nullable=True))
    op.alter_column('newsletters', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('newsletters_email_key', 'newsletters', type_='unique')
    op.drop_column('newsletters', 'email')
    op.alter_column('notifications', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('products', sa.Column('category_id', sa.String(), nullable=False))
    op.add_column('products', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('image_url', sa.String(), nullable=False))
    op.add_column('products', sa.Column('status', sa.Enum('in_stock', 'out_of_stock', 'low_on_stock', name='productstatusenum'), nullable=True))
    op.add_column('products', sa.Column('archived', sa.Boolean(), nullable=True))
    op.add_column('products', sa.Column('filter_status', sa.Enum('published', 'draft', name='productfilterstatusenum'), nullable=True))
    op.create_foreign_key(None, 'products', 'product_categories', ['category_id'], ['id'], ondelete='CASCADE')
    op.alter_column('profiles', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('profiles', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_url')
    op.alter_column('profiles', 'updated_at',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('profiles', 'created_at',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'filter_status')
    op.drop_column('products', 'archived')
    op.drop_column('products', 'status')
    op.drop_column('products', 'image_url')
    op.drop_column('products', 'quantity')
    op.drop_column('products', 'category_id')
    op.alter_column('notifications', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('newsletters', sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    op.create_unique_constraint('newsletters_email_key', 'newsletters', ['email'])
    op.alter_column('newsletters', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('newsletters', 'description')
    op.drop_column('billing_plans', 'description')
    op.drop_column('billing_plans', 'duration')
    op.create_table('user_newsletter_association',
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('newsletter_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['newsletter_id'], ['newsletters.id'], name='user_newsletter_association_newsletter_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_newsletter_association_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'newsletter_id', name='user_newsletter_association_pkey')
    )
    op.drop_index(op.f('ix_product_variants_id'), table_name='product_variants')
    op.drop_table('product_variants')
    op.drop_index(op.f('ix_notification_settings_id'), table_name='notification_settings')
    op.drop_table('notification_settings')
    op.drop_index(op.f('ix_newsletter_subscribers_id'), table_name='newsletter_subscribers')
    op.drop_table('newsletter_subscribers')
    op.drop_index(op.f('ix_topics_id'), table_name='topics')
    op.drop_table('topics')
    op.drop_index(op.f('ix_product_categories_id'), table_name='product_categories')
    op.drop_table('product_categories')
    op.drop_index(op.f('ix_faqs_id'), table_name='faqs')
    op.drop_table('faqs')
    # ### end Alembic commands ###

from fasthtml.common import *
from db import SessionLocal
from models import Artwork, ArtworkStatus


def artwork_card_investor(a):
    status_cls = 'bg-green-100 text-green-800' if a.status.value == 'active' else 'bg-blue-100 text-blue-800'
    status_label = 'Open for Investment' if a.status.value == 'active' else 'Fully Funded'
    return Div(
        Div(
            Img(src=a.image_url, alt=a.title,
                cls='w-full h-56 object-cover') if a.image_url else
            Div('No Image', cls='w-full h-56 bg-gray-100 flex items-center justify-center text-gray-400 text-sm'),
            Span(status_label, cls=f'absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold {status_cls}'),
            cls='relative overflow-hidden rounded-t-xl'
        ),
        Div(
            P(a.artist_name or 'Unknown Artist', cls='text-xs text-primary font-semibold uppercase tracking-wider mb-1'),
            H3(a.title, cls='text-lg font-bold text-gray-900 mb-2 leading-tight'),
            Div(
                Span(a.category.value.replace('_', ' ').title(), cls='text-xs bg-blue-50 text-primary px-2 py-1 rounded'),
                Span(f'{a.origin_country}', cls='text-xs text-gray-400') if a.origin_country else '',
                cls='flex items-center gap-2 mb-3'
            ),
            Div(
                Div(
                    P('Estimated Value', cls='text-xs text-gray-400'),
                    P(f'€{a.estimated_value:,.0f}' if a.estimated_value else 'TBD', cls='text-base font-bold text-gray-900'),
                ),
                Div(
                    P('Target Return', cls='text-xs text-gray-400'),
                    P(f'{a.appreciation_rate}% p.a.' if a.appreciation_rate else 'TBD', cls='text-base font-bold text-primary'),
                ),
                cls='grid grid-cols-2 gap-4 mb-4'
            ),
            A('Invest Now', href='/register',
              cls='block text-center px-6 py-2.5 rounded-full font-semibold text-sm bg-primary text-white hover:bg-primary-dark transition-colors no-underline')
            if a.status.value == 'active' else
            Span('Fully Funded', cls='block text-center px-6 py-2.5 rounded-full font-semibold text-sm bg-gray-100 text-gray-500'),
            cls='p-6'
        ),
        cls='bg-white rounded-xl border border-gray-200 overflow-hidden hover:-translate-y-1 hover:shadow-lg transition-all'
    )


def investors_page():
    hero = Section(
        Div(
            H1('Invest in Fine Art', cls='font-display text-4xl font-extrabold text-white mb-4'),
            P('Own fractional shares of blue-chip artworks by the world\'s most sought-after artists. '
              'Diversify your portfolio with an asset class that has outperformed global equities over the past 25 years.',
              cls='text-lg text-white/90 max-w-2xl'),
            cls='max-w-7xl mx-auto relative z-10'
        ),
        cls='art-gradient py-16 px-8'
    )

    benefits = Section(
        Div(
            Div(
                H2('Why Invest With Kanvas.ai', cls='font-display text-3xl font-bold text-gray-900 mb-4'),
                P('Tangible, appreciating assets with institutional-grade security.', cls='text-base text-gray-500 max-w-xl mx-auto'),
                cls='text-center mb-12'
            ),
            Div(
                Div(
                    H3('Strong Historical Returns', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Blue-chip art has appreciated at 13.8% annually over the past 25 years. Our curated offerings target 10\u201318% annualised returns.',
                      cls='text-gray-500 text-sm leading-relaxed'),
                    cls='bg-white rounded-lg p-8 border border-gray-200 hover:-translate-y-1 hover:shadow-md transition-all'
                ),
                Div(
                    H3('Physical Asset Security', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Every investment is backed by a real artwork, professionally appraised, fully insured, and stored in museum-grade facilities across Europe.',
                      cls='text-gray-500 text-sm leading-relaxed'),
                    cls='bg-white rounded-lg p-8 border border-gray-200 hover:-translate-y-1 hover:shadow-md transition-all'
                ),
                Div(
                    H3('Portfolio Diversification', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Art shows low correlation to stocks and bonds. Add an uncorrelated asset class to reduce overall portfolio volatility.',
                      cls='text-gray-500 text-sm leading-relaxed'),
                    cls='bg-white rounded-lg p-8 border border-gray-200 hover:-translate-y-1 hover:shadow-md transition-all'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='max-w-7xl mx-auto'
        ),
        cls='py-20 px-8 bg-blue-50'
    )

    # Fetch artworks from DB
    db = SessionLocal()
    try:
        artworks = db.query(Artwork).filter(
            Artwork.status.in_([ArtworkStatus.active, ArtworkStatus.funded])
        ).order_by(Artwork.id.desc()).all()
        cards = [artwork_card_investor(a) for a in artworks]
    finally:
        db.close()

    listings = Section(
        Div(
            Div(
                H2('Current Offerings', cls='font-display text-3xl font-bold text-gray-900 mb-4'),
                P('Browse our curated selection of investment-grade artworks.', cls='text-base text-gray-500 max-w-xl mx-auto'),
                cls='text-center mb-12'
            ),
            Div(*cards, cls='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8') if cards else
            P('No artworks currently available. Check back soon.', cls='text-gray-500 text-center'),
            cls='max-w-7xl mx-auto'
        ),
        cls='py-20 px-8'
    )

    investment_options = Section(
        Div(
            Div(
                H2('Investment Options', cls='font-display text-3xl font-bold text-white mb-4'),
                P('Choose the approach that suits your style.', cls='text-base text-blue-100 max-w-xl mx-auto'),
                cls='text-center mb-12'
            ),
            Div(
                Div(
                    H3('Auto Invest', cls='text-accent mb-4 text-lg font-bold'),
                    P('Set your criteria and let our algorithm build your art portfolio.', cls='mb-6 text-gray-500 text-sm'),
                    Div(
                        P('\u2713 Automated portfolio diversification', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Custom risk and category preferences', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Spread across artists and periods', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Reinvestment of sale proceeds', cls='mb-2 text-sm text-gray-500'),
                    ),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Curated Selection', cls='text-primary mb-4 text-lg font-bold'),
                    P('Browse and select individual artworks from our gallery.', cls='mb-6 text-gray-500 text-sm'),
                    Div(
                        P('\u2713 Full control over your collection', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Detailed provenance and appraisals', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Choose by artist, period, medium', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Real-time valuation tracking', cls='mb-2 text-sm text-gray-500'),
                    ),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Secondary Market', cls='text-blue-300 mb-4 text-lg font-bold'),
                    P('Buy and sell existing fractional positions.', cls='mb-6 text-gray-500 text-sm'),
                    Div(
                        P('\u2713 Added liquidity for your holdings', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Access seasoned investments', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Adjust portfolio anytime', cls='mb-2 text-sm text-gray-500'),
                        P('\u2713 Market-driven pricing', cls='mb-2 text-sm text-gray-500'),
                    ),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='max-w-7xl mx-auto'
        ),
        cls='bg-primary-dark text-white py-20 px-8'
    )

    key_figures = Section(
        Div(
            Div(
                H2('Investment at a Glance', cls='font-display text-3xl font-bold text-gray-900 mb-4'),
                cls='text-center mb-12'
            ),
            Div(
                Div(H3('\u20ac500', cls='text-3xl font-extrabold text-primary mb-1'), P('Minimum Investment', cls='text-xs text-gray-500 uppercase tracking-wider'), cls='text-center'),
                Div(H3('10\u201318%', cls='text-3xl font-extrabold text-primary mb-1'), P('Target Returns', cls='text-xs text-gray-500 uppercase tracking-wider'), cls='text-center'),
                Div(H3('3\u201310 yr', cls='text-3xl font-extrabold text-primary mb-1'), P('Hold Period', cls='text-xs text-gray-500 uppercase tracking-wider'), cls='text-center'),
                Div(H3('180+', cls='text-3xl font-extrabold text-primary mb-1'), P('Artworks Funded', cls='text-xs text-gray-500 uppercase tracking-wider'), cls='text-center'),
                cls='max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8'
            ),
            cls='max-w-7xl mx-auto'
        ),
        cls='py-20 px-8 bg-blue-50'
    )

    cta = Section(
        Div(
            H2('Start Building Your Art Portfolio', cls='font-display text-3xl mb-4'),
            P('Create your free account and invest in your first artwork in minutes.',
              cls='text-lg text-white/90 max-w-xl mx-auto mb-8'),
            A('Create Account', href='/register',
              cls='inline-block px-8 py-3 rounded-full font-semibold text-base no-underline bg-white text-primary hover:bg-blue-50 transition-colors'),
        ),
        cls='art-gradient text-white py-20 px-8 text-center'
    )

    return Div(hero, benefits, listings, investment_options, key_figures, cta)

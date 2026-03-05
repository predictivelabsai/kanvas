from fasthtml.common import *


def contact_page():
    hero = Section(
        Div(
            H1('Contact Us', cls='font-display text-4xl font-extrabold text-white mb-4'),
            P('Get in touch with our team. We are here to help with any questions about investing or consigning through Kanvas.ai.',
              cls='text-lg text-white/90 max-w-2xl'),
            cls='max-w-7xl mx-auto relative z-10'
        ),
        cls='art-gradient py-16 px-8'
    )

    offices = Section(
        Div(
            Div(
                H2('Our Offices', cls='font-display text-3xl font-bold text-gray-900 mb-4'),
                cls='text-center mb-12'
            ),
            Div(
                Div(
                    H3('London (HQ)', cls='text-lg font-bold text-gray-900 mb-3'),
                    P(Strong('Address'), Br(),
                      '12 Mason\'s Yard', Br(),
                      'St James\'s', Br(),
                      'London SW1Y 6BU', Br(),
                      'United Kingdom', cls='mb-4 text-sm text-gray-600 leading-relaxed'),
                    P(Strong('Email'), Br(),
                      A('london@kanvas.ai', href='mailto:london@kanvas.ai',
                        cls='text-black no-underline'), cls='mb-4 text-sm'),
                    P(Strong('Phone'), Br(),
                      A('+44 20 7123 4567', href='tel:+442071234567',
                        cls='text-black no-underline'), cls='text-sm'),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Paris', cls='text-lg font-bold text-gray-900 mb-3'),
                    P(Strong('Address'), Br(),
                      '8 Rue de Turenne', Br(),
                      'Le Marais', Br(),
                      '75004 Paris', Br(),
                      'France', cls='mb-4 text-sm text-gray-600 leading-relaxed'),
                    P(Strong('Email'), Br(),
                      A('paris@kanvas.ai', href='mailto:paris@kanvas.ai',
                        cls='text-black no-underline'), cls='mb-4 text-sm'),
                    P(Strong('Phone'), Br(),
                      A('+33 1 42 78 56 00', href='tel:+33142785600',
                        cls='text-black no-underline'), cls='text-sm'),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Zurich', cls='text-lg font-bold text-gray-900 mb-3'),
                    P(Strong('Address'), Br(),
                      'Bahnhofstrasse 28', Br(),
                      '8001 Z\u00fcrich', Br(),
                      'Switzerland', cls='mb-4 text-sm text-gray-600 leading-relaxed'),
                    P(Strong('Email'), Br(),
                      A('zurich@kanvas.ai', href='mailto:zurich@kanvas.ai',
                        cls='text-black no-underline'), cls='mb-4 text-sm'),
                    P(Strong('Phone'), Br(),
                      A('+41 44 210 12 34', href='tel:+41442101234',
                        cls='text-black no-underline'), cls='text-sm'),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='max-w-7xl mx-auto'
        ),
        cls='py-20 px-8 bg-[#FAFAFA]'
    )

    general = Section(
        Div(
            Div(
                H2('General Enquiries', cls='font-display text-3xl font-bold text-white mb-4'),
                cls='text-center mb-12'
            ),
            Div(
                Div(
                    H3('Investor Support', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Questions about your account, investments, or portfolio?', cls='text-gray-500 text-sm mb-4'),
                    P(A('investors@kanvas.ai', href='mailto:investors@kanvas.ai',
                        cls='text-accent no-underline font-semibold')),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Consignment Enquiries', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Want to consign artwork or have questions about the process?', cls='text-gray-500 text-sm mb-4'),
                    P(A('consign@kanvas.ai', href='mailto:consign@kanvas.ai',
                        cls='text-accent no-underline font-semibold')),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                Div(
                    H3('Press & Media', cls='text-lg font-bold text-gray-900 mb-3'),
                    P('Media enquiries, partnership opportunities, or press information?', cls='text-gray-500 text-sm mb-4'),
                    P(A('press@kanvas.ai', href='mailto:press@kanvas.ai',
                        cls='text-accent no-underline font-semibold')),
                    cls='bg-white rounded-lg p-8 border border-gray-200'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='max-w-7xl mx-auto'
        ),
        cls='bg-black text-white py-20 px-8'
    )

    return Div(hero, offices, general)

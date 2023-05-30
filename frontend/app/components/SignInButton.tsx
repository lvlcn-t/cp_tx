'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useSession, signIn, signOut } from 'next-auth/react'
import { Menu, Transition } from '@headlessui/react'
import clsx from 'clsx'
import React from 'react'

const SignInButton : React.FC = () => {
    const { data: session } = useSession()

    return (
        <>
            {
              session ? (
                <Menu as='div' className='relative'>
                    <Menu.Button>
                        {
                        session?.user?.image ? (
                            <div className='relative h-10 w-10'>
                                <Image
                                    src={session.user.image}
                                    alt={session.user.name}
                                    className='inline-block rounded-full'
                                    fill
                                />
                            </div>
                        
                        ) : (
                        <span className='inline-block h-8 w-8 overflow-hidden rounded-full'>
                            <svg
                            className='h-full w-full text-stone-300'
                            fill='currentColor'
                            viewBox='0 0 24 24'
                            >
                                <path d=''/>
                            </svg>
                        </span>
                        )
                    }
                    </Menu.Button>
                    <Transition
                        enter='transition duration-150 ease-out'
                        enterFrom='transform scale-95 opacity-0'
                        enterTo='transform scale-100 opacity-100'
                        leave='transition duration-150 ease-out'
                        leaveFrom='transform scale-100 opacity-100'
                        leaveTo='transform scale-95 opacity-0'
                    >
                      <Menu.Items className='bg-react dark:text-react absolute right-0.5'>
                        <div className='mb-4 flex px-6 text-sm'>
                            {session?.user?.image ? (
                                <div className='relative h-10 w-10'>
                                <Image
                                    src={session.user.image}
                                    alt={session.user.name}
                                    className='inline-block rounded-full'
                                    fill
                                />
                            </div>
                            ) : (
                            <span className='inline-block h-8 w-8 overflow-hidden rounded-full'>
                                <svg
                                className='h-full w-full text-stone-300'
                                fill='currentColor'
                                viewBox='0 0 24 24'
                                >
                                    <path d=''/>
                                </svg>
                            </span>
                            )}
                            <div>
                                <p className='font-medium text-stone-600'>
                                    {session.user.name || 'User name'}
                                </p>
                                <p className='text-stone-400'>{session.user.email}</p>
                            </div>
                        </div>
                        <Menu.Item>
                            {({ active }) => (
                                <Link
                                href='/profile'
                                className={clsx(
                                    active && 'bg-stone-700/50 dark:bg-stone-200',
                                    'inline-flex items-center gap-6 px-[34px] py-2 text-sm'
                                )}
                                >
                                    <Cog8ToothIcon className='h-5 w-5 text-stone-400' />
                                    <span>Manage Account</span>
                                </Link>
                            )}
                        </Menu.Item>
                        <Menu.Item>
                            {({ active }) => (
                                <button
                                className={clsx(
                                    active && 'bg-stone-700/50 dark:bg-stone-200',
                                    'inline-flex items-center gap-6 px-[34px] py-2 text-sm'
                                )}
                                onClick={() => signOut()}
                                >
                                    <ArrowRightOnRectangleIcon className='h-5 w-5 text-stone-400' />
                                    <span>Manage Account</span>
                                </button>
                            )}
                        </Menu.Item>
                      </Menu.Items>
                    </Transition>
                </Menu>
              ) : (
                <button
                className='rounded-md border border-stone-300 px-3 py-1 text-sm'
                onClick={() => signIn()}
                >
                  Sign In
                </button>
              )
            }
        </>
    )
} 

export default SignInButton;